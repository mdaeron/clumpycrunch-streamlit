#! /usr/bin/env python3
"""
Try streamlit
"""

import streamlit as st
import pandas as pd

st.write("""
# ClumpyCrunch

### Input data

Paste your raw data here:
""")

df = pd.DataFrame({
	'UID':     pd.Series([''], dtype = 'str'),
	'Session': pd.Series([], dtype = 'str'),
	'Sample':  pd.Series([], dtype = 'str'),
	'd45':     pd.Series([], dtype = 'float'),
	'd46':     pd.Series([], dtype = 'float'),
	'd47':     pd.Series([], dtype = 'float'),
	'd48':     pd.Series([], dtype = 'float'),
	'd49':     pd.Series([], dtype = 'float'),
	})

rawdata = st.data_editor(
	df,
	num_rows = 'dynamic',
	use_container_width = True,
	)

rawdata = rawdata.to_dict('records')
rawdata = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in rawdata]

rawdata

D47_anchors_expander = st.expander('Δ47 Anchors')
with D47_anchors_expander:
	st.write("### Δ47 Anchors")

	D47anchors_df = pd.DataFrame({
		'Sample':  pd.Series([], dtype = 'str'),
		'NominalD47':     pd.Series([], dtype = 'float'),
		})

	D47anchors = st.data_editor(
		D47anchors_df,
		num_rows = 'dynamic',
		use_container_width = True,
		)

	D47anchors = D47anchors.to_dict('records')
	D47anchors = [{k: r[k] for k in r if not pd.isnull(r[k])} for r in D47anchors]
	
	D47anchors
	

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