#! /usr/bin/env python3
"""
Try streamlit
"""

__version__ = 0.1

import io, zipfile, D47crunch
import pandas as pd
from datetime import datetime as dt
import streamlit as st

st.set_page_config(
	page_title = 'ClumpyCrunch',
	layout = 'wide',
	)

st.write('''
<style>
h1 {
	background-color: #fdcf4e;
	margin-top: 0;
	}
h2, h3 {
	background-color: #F0F0F0;	
}
h1, h2, h3 {
	padding-left: 0.6em;
	padding-top: 0.4ex;
	padding-bottom: 0.4ex;
	margin-bottom: 1ex;
}
</style>
''', unsafe_allow_html = True)

st.write("""
# ClumpyCrunch

Experimental implementation using streamlit

### Input data
Paste your raw data here:
""")

rawdata_df = pd.DataFrame({
	'UID':     pd.Series([None], dtype = 'str'),
	'Session': pd.Series([None], dtype = 'str'),
	'Sample':  pd.Series([None], dtype = 'str'),
	'd45':     pd.Series([None], dtype = 'float'),
	'd46':     pd.Series([None], dtype = 'float'),
	'd47':     pd.Series([None], dtype = 'float'),
	'd48':     pd.Series([None], dtype = 'float'),
	'd49':     pd.Series([None], dtype = 'float'),
	})

rawdata_df = st.data_editor(
	rawdata_df,
	num_rows = 'dynamic',
	use_container_width = True,
	hide_index = True,
	column_config = {
		k: st.column_config.NumberColumn(format = '%.4f')
		for k in ['d45', 'd46', 'd47', 'd48', 'd49']
		},
	)

rawdata = rawdata_df.to_dict('records')
rawdata = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in rawdata]

st.write("### Data reduction parameters")

isoparams = [
	(
		'R13_VPDB',
		0.01118,
		'13C/12C ratio of VPDB',
		),
	(
		'R18_VSMOW',
		0.0020052,
		'18O/16O ratio of VSMOW',
		),
	(
		'R17_VSMOW',
		0.00038475,
		'17O/16O ratio of VSMOW',
		),
	(
		'lambda_17',
		0.528,
		'Triple oxygen isotope exponent',
		),
	(
		'alpha_18_acid',
		1.008129,
		'18O/16O fractionation factor of acid reaction',
		),
	]

isoparams_df = pd.DataFrame({
	'Parameter':  pd.Series([_[0] for _ in isoparams],    dtype = 'str'),
	'Definition': pd.Series([_[2] for _ in isoparams],    dtype = 'str'),
	'Value':      pd.Series([_[1] for _ in isoparams],    dtype = 'str'),
	})

isoparams_df = st.data_editor(
	isoparams_df,
	num_rows = 5,
	use_container_width = False,
	hide_index = True,
	disabled = ('Parameter', 'Definition'),
	)

isoparams = {r['Parameter']: float(r['Value']) for r in isoparams_df.to_dict('records')}

st.write("""
### Reference Materials
The following samples are used as anchors to standardize δ<sup>13</sup>C<sub>VPDB</sub>, δ<sup>18</sup>O<sub>VPDB</sub>, Δ<sub>47</sub>, and Δ<sub>48</sub> values:
""", unsafe_allow_html = True)

anchors = {}

for s in D47crunch.D4xdata().Nominal_d13C_VPDB:
	if s not in anchors:
		anchors[s] = {}
	anchors[s]['d13C_VPDB'] = f'{D47crunch.D4xdata().Nominal_d13C_VPDB[s]:.2f}'

for s in D47crunch.D4xdata().Nominal_d18O_VPDB:
	if s not in anchors:
		anchors[s] = {}
	anchors[s]['d18O_VPDB'] = f'{D47crunch.D4xdata().Nominal_d18O_VPDB[s]:.2f}'

for s in D47crunch.D47data().Nominal_D47:
	if s not in anchors:
		anchors[s] = {}
	anchors[s]['D47'] = f'{D47crunch.D47data().Nominal_D47[s]:.4f}'

for s in D47crunch.D48data().Nominal_D48:
	if s not in anchors:
		anchors[s] = {}
	anchors[s]['D48'] = f'{D47crunch.D48data().Nominal_D48[s]:.3f}'

anchors_df = pd.DataFrame({
	'Sample':    pd.Series([s for s in anchors], dtype = 'str'),
	'd13C_VPDB': pd.Series([anchors[s]['d13C_VPDB'] if 'd13C_VPDB' in anchors[s] else None for s in anchors], dtype = 'str'),
	'd18O_VPDB': pd.Series([anchors[s]['d18O_VPDB'] if 'd18O_VPDB' in anchors[s] else None for s in anchors], dtype = 'str'),
	'D47':       pd.Series([anchors[s]['D47'] if 'D47' in anchors[s] else None for s in anchors], dtype = 'str'),
	'D48':       pd.Series([anchors[s]['D48'] if 'D48' in anchors[s] else None for s in anchors], dtype = 'str'),
	})

anchors = st.data_editor(
	anchors_df,
	num_rows = 'dynamic',
	use_container_width = False,
	hide_index = True,
	)

anchors = anchors.to_dict('records')
anchors = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in anchors]


st.write("### Standardization of bulk composition :red[(not editable yet)]")

d1xX_stdz_df = pd.DataFrame({
		'Quantity':     pd.Series(['δ13C', 'δ18O'],    dtype = 'str'),
		'Method':     pd.Series(['Affine transformation', 'Affine transformation'],    dtype = 'str'),
		})

d1xX_stdz_methods = st.data_editor(
	d1xX_stdz_df,
	num_rows = 2,
	use_container_width = False,
	hide_index = True,
	disabled = ('Quantity',),
	column_config = {
		'Method': st.column_config.SelectboxColumn(
			'Method',
			help = 'Which standardization method to use',
			width = 'medium',
			required = True,
			options=['Affine transformation', 'Constant offset'],
			)
		},
	)

st.write("### Standardization of clumped isotopes :red[(not editable yet)]")

D4x_stdz_methods = st.data_editor(
	pd.DataFrame({
		'Quantity':     pd.Series(['Δ47', 'Δ48'],    dtype = 'str'),
		'Method':     pd.Series(['Pooled regression', 'Pooled regression'],    dtype = 'str'),
		}),
	num_rows = 2,
	use_container_width = False,
	hide_index = True,
	disabled = ('Quantity',),
	column_config = {
		'Method': st.column_config.SelectboxColumn(
			'Method',
			help = 'Which standardization method to use',
			width = 'medium',
			required = True,
			options=['Pooled regression', 'Independent sessions'],
			)
		},
	)

# df = pd.DataFrame(
# 	[
# 		{
# 			'd13C_stdz_method': 'Affine transformation',
# 			'd18O_stdz_method': 'Affine transformation',
# 			'D47_stdz_method':  'Pooled',
# 			'D48_stdz_method':  'Pooled',
# 		}
# 	]
# )

# for k in ['D47_stdz_method', 'D48_stdz_method']:
# 	df[k] = (df[k].astype('category').cat.add_categories(['Independent sessions']))

# edited_df = st.data_editor(
# 	df,
# 	hide_index = True,
# # 	disabled = [],
# 	)


process_button = st.button(':red[Process data]')
st.write(':red[(Δ48 not yet implemented)]')

if process_button:
	rawdata47 = D47crunch.D47data(rawdata)

	rawdata47.R13_VPDB = isoparams['R13_VPDB']
	rawdata47.R18_VSMOW = isoparams['R18_VSMOW']
	rawdata47.R17_VSMOW = isoparams['R17_VSMOW']
	rawdata47.LAMBDA_17 = isoparams['lambda_17']
	rawdata47.R18_VPDB = rawdata47.R18_VSMOW * 1.03092
	rawdata47.R17_VPDB = rawdata47.R17_VSMOW * 1.03092 ** rawdata47.LAMBDA_17

	rawdata47.Nominal_d13C_VPDB = {a['Sample']: float(a['d13C_VPDB']) for a in anchors if 'd13C_VPDB' in a}
	rawdata47.Nominal_d18O_VPDB = {a['Sample']: float(a['d18O_VPDB']) for a in anchors if 'd18O_VPDB' in a}
	rawdata47.Nominal_D47 = {a['Sample']: float(a['D47']) for a in anchors if 'D47' in a}
	rawdata47.refresh()
	rawdata47.wg()
	rawdata47.crunch()
	rawdata47.standardize()

	st.write('### Results')

	st.write('#### Table of samples')
	table_of_samples = D47crunch.table_of_samples(rawdata47, output = 'raw')
	st.data_editor(
		pd.DataFrame(
			table_of_samples[1:],
			columns = table_of_samples[0],
			),
		hide_index = True,
		disabled = table_of_samples[0],
		)

	st.write('#### Table of sessions')
	table_of_sessions = D47crunch.table_of_sessions(rawdata47, output = 'raw')
	st.data_editor(
		pd.DataFrame(
			table_of_sessions[1:],
			columns = table_of_sessions[0],
			),
		hide_index = True,
		disabled = table_of_sessions[0],
		)

	st.write('#### Table of analyses')
	table_of_analyses = D47crunch.table_of_analyses(rawdata47, output = 'raw')
	st.data_editor(
		pd.DataFrame(
			table_of_analyses[1:],
			columns = table_of_analyses[0],
			),
		hide_index = True,
		disabled = table_of_analyses[0],
		)
	
	st.write('#### Sessions plots')
	for session in rawdata47.sessions:
		sp = rawdata47.plot_single_session(session, xylimits = 'constant')
		st.pyplot(sp.fig, use_container_width = False, dpi = 72)

	buf = io.BytesIO()

	readme = f'''
ClumpyCrunch version {__version__}, using D47crunch version {D47crunch.__version__}
Processed on {dt.now().strftime('%Y-%m-%d %H:%M:%S')}

Contents:

* analyses.csv  : table of analyses
* anchors.csv   : table of the anchors used to standardize δ13C, δ18O, Δ47, and Δ48 measurements
* isoparams.csv : table of the parameters used for data reduction
* rawdata.csv   : table of the raw input data, before any standardization
'''

	with zipfile.ZipFile(buf, 'x') as csv_zip:
		csv_zip.writestr('analyses.csv', '\n'.join([','.join(l) for l in table_of_analyses]))
		csv_zip.writestr('anchors.csv', anchors_df.to_csv(index = False))
		csv_zip.writestr('isoparams.csv', isoparams_df.to_csv(index = False))
		csv_zip.writestr('rawdata.csv', rawdata_df.to_csv(index = False))
		csv_zip.writestr('readme.txt', readme[1:])

	st.download_button(
		label = 'Download zip',
		data = buf.getvalue(),
		file_name = 'clumpycrunch-results.zip',
		mime = 'application/zip',
		)

st.write(f'''
<div style="color:#999999; margin-top:4ex;">
<a style="color:inherit" href="https://github.com/mdaeron/clumpycrunch-streamlit">ClumpyCrunch</a>
is an open-source web app based on the
<a style="color:inherit" href="https://github.com/mdaeron/D47crunch">D47crunch</a>
library, using standardization and error propagation methods described by
<a style="color:inherit" href="https://doi.org/10.1029/2020GC009592">Daëron (2021)</a>.

<p>
Please <a style="color:inherit" href="https://github.com/mdaeron/clumpycrunch-streamlit/issues">open an issue</a>
for bug reports, questions and/or suggestions.
</div>
''', unsafe_allow_html = True)


# A01	Session01	ETH-1	5.795017	11.627668	16.893512	11.491072	17.277490
# A02	Session01	FOO-1	6.219070	11.491072	17.277490	-4.817179	-11.635064
# A03	Session01	ETH-2	-6.058681	-4.817179	-11.635064	4.941839	0.606117
# A04	Session01	FOO-2	-3.861839	4.941839	0.606117	12.052277	17.405548
# A05	Session01	ETH-3	5.543654	12.052277	17.4055482	-2.087501	-39.548484
# A06	Session01	MERCK	-35.929352	-2.087501	-39.548484	-5.194170	-11.944111
# A07	Session01	ETH-4	-6.222218	-5.194170	-11.944111	-4.877104	-11.699265
# A08	Session01	ETH-2	-6.067055	-4.877104	-11.6992659	-2.080798	-39.545632
# A09	Session01	MERCK	-35.930739	-2.080798	-39.545632	11.559104	16.801908
# A10	Session01	ETH-1	5.788207	11.559104	16.801908	-5.221407	-11.987503
# A11	Session01	ETH-4	-6.217508	-5.221407	-11.987503	4.868892	0.521845
# A12	Session01	FOO-2	-3.876921	4.868892	0.521845	12.013444	17.368631
# A13	Session01	ETH-3	5.539840	12.013444	17.368631	11.447846	17.234280
# A14	Session01	FOO-1	6.219046	11.447846	17.234280	-4.817179	-11.635064
# B01	Session02	ETH-1	5.795017	11.627668	16.893512	11.491072	17.277490
# B02	Session02	FOO-1	6.219070	11.491072	17.277490	-4.817179	-11.635064
# B03	Session02	ETH-2	-6.058681	-4.817179	-11.635064	4.941839	0.606117
# B04	Session02	FOO-2	-3.861839	4.941839	0.606117	12.052277	17.405548
# B05	Session02	ETH-3	5.543654	12.052277	17.4055482	-2.087501	-39.548484
# B06	Session02	MERCK	-35.929352	-2.087501	-39.548484	-5.194170	-11.944111
# B07	Session02	ETH-4	-6.222218	-5.194170	-11.944111	-4.877104	-11.699265
# B08	Session02	ETH-2	-6.067055	-4.877104	-11.6992659	-2.080798	-39.545632
# B09	Session02	MERCK	-35.930739	-2.080798	-39.545632	11.559104	16.801908
# B10	Session02	ETH-1	5.788207	11.559104	16.801908	-5.221407	-11.987503
# B11	Session02	ETH-4	-6.217508	-5.221407	-11.987503	4.868892	0.521845
# B12	Session02	FOO-2	-3.876921	4.868892	0.521845	12.013444	17.368631
# B13	Session02	ETH-3	5.539840	12.013444	17.368631	11.447846	17.234280
# B14	Session02	FOO-1	6.219046	11.447846	17.234280	-4.817179	-11.635064