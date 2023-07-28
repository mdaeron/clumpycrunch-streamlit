#! /usr/bin/env python3
"""
Try streamlit
"""

import streamlit as st
import pandas as pd

st.set_page_config(
	page_title = 'ClumpyCrunch',
	layout = 'wide',
	)

st.write("""
# ClumpyCrunch
### Input data
Paste your raw data here:
""")


rawdata = st.data_editor(
	pd.DataFrame({
		'UID':     pd.Series([], dtype = 'str'),
		'Session': pd.Series([], dtype = 'str'),
		'Sample':  pd.Series([], dtype = 'str'),
		'd45':     pd.Series([], dtype = 'float'),
		'd46':     pd.Series([], dtype = 'float'),
		'd47':     pd.Series([], dtype = 'float'),
		'd48':     pd.Series([], dtype = 'float'),
		'd49':     pd.Series([], dtype = 'float'),
		}),
	num_rows = 'dynamic',
	use_container_width = True,
	hide_index = True,
	)

rawdata = rawdata.to_dict('records')
rawdata = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in rawdata]

# D47_anchors_expander = st.expander('Standardization Anchors')
# with D47_anchors_expander:

st.write("""
### Standardization Anchors
The following samples are used as anchors to standardize δ<sup>13</sup>C<sub>VPDB</sub>, δ<sup>18</sup>O<sub>VPDB</sub>, Δ<sub>47</sub>, and Δ<sub>48</sub> values:
""", unsafe_allow_html = True)

anchors_df = pd.DataFrame({
	'Sample':    pd.Series([], dtype = 'str'),
	'd13C_VPDB': pd.Series([], dtype = 'float'),
	'd18O_VPDB': pd.Series([], dtype = 'float'),
	'D47':       pd.Series([], dtype = 'float'),
	'D48':       pd.Series([], dtype = 'float'),
	})

anchors = st.data_editor(
	anchors_df,
	num_rows = 'dynamic',
	use_container_width = True,
	hide_index = True,
	)

anchors = anchors.to_dict('records')
anchors = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in anchors]

st.write("### Oxygen-17 correction parameters and acid fractionation of oxygen-18")

isoparams = st.data_editor(
	pd.DataFrame({
		'Parameter':     pd.Series(['R13_VPDB', 'R18_VSMOW', 'R17_VSMOW', 'lambda_17', 'alpha18_acid'],    dtype = 'str'),
		'Value':     pd.Series([0.01118, 0.0020052, 0.00038475, 0.528, 1.008129],    dtype = 'str'),
		}),
	num_rows = 5,
	use_container_width = False,
	hide_index = True,
	disabled = ('Parameter',),
	)

isoparams = {r['Parameter']: float(r['Value']) for r in isoparams.to_dict('records')}

st.write("#### Standardization methods:")

stdz_methods = st.data_editor(
	pd.DataFrame({
		'Quantity':     pd.Series(['δ13C', 'δ18O', 'Δ47', 'Δ48'],    dtype = 'str'),
		'Method':     pd.Series(['Affine transformation', 'Affine transformation', 'Pooled regression', 'Pooled regression'],    dtype = 'str'),
		}),
	num_rows = 4,
	use_container_width = False,
	hide_index = True,
	disabled = ('Quantity',),
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

# for k in ['d13C_stdz_method', 'd18O_stdz_method']:
# 	df[k] = (df[k].astype('category').cat.add_categories(['Constant offset']))
# for k in ['D47_stdz_method', 'D48_stdz_method']:
# 	df[k] = (df[k].astype('category').cat.add_categories(['Independent sessions']))

# edited_df = st.data_editor(
# 	df,
# 	hide_index = True,
# # 	disabled = [],
# 	)


# A01	Session01	ETH-1	5.795017	11.627668	16.893512	11.491072	17.277490
# A02	Session01	IAEA-C1	6.219070	11.491072	17.277490	-4.817179	-11.635064
# A03	Session01	ETH-2	-6.058681	-4.817179	-11.635064	4.941839	0.606117
# A04	Session01	IAEA-C2	-3.861839	4.941839	0.606117	12.052277	17.405548
# A05	Session01	ETH-3	5.543654	12.052277	17.4055482	-2.087501	-39.548484
# A06	Session01	MERCK	-35.929352	-2.087501	-39.548484	-5.194170	-11.944111
# A07	Session01	ETH-4	-6.222218	-5.194170	-11.944111	-4.877104	-11.699265
# A08	Session01	ETH-2	-6.067055	-4.877104	-11.6992659	-2.080798	-39.545632
# A09	Session01	MERCK	-35.930739	-2.080798	-39.545632	11.559104	16.801908
# A10	Session01	ETH-1	5.788207	11.559104	16.801908	-5.221407	-11.987503
# A11	Session01	ETH-4	-6.217508	-5.221407	-11.987503	4.868892	0.521845
# A12	Session01	IAEA-C2	-3.876921	4.868892	0.521845	12.013444	17.368631
# A13	Session01	ETH-3	5.539840	12.013444	17.368631	11.447846	17.234280
# A14	Session01	IAEA-C1	6.219046	11.447846	17.234280	-4.817179	-11.635064