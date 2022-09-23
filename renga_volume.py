# %%
from shroomdk import ShroomDK
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# %%
# Initialize `ShroomDK` with your API Key
sdk = ShroomDK("7d45ba9b-a130-4537-a45a-8493e706edae")
st.set_page_config(layout='wide')

# %%
# Parameters can be passed into SQL statements 
# via native string interpolation
my_address = ("0x2F8D8846C376bC842Cd9B904C9b505e39A6c54Dc")
sql = f"""
            select 
            date_trunc('day', block_timestamp) as day,
            sum(price),
            sum(case when nft_address in ('0x394e3d3044fc89fcdd966d3cb35ac0b32b0cda91','0x64ad353bc90a04361c4810ae7b3701f3beb48d7e','0x5bd815fd6c096bab38b4c6553cfce3585194dff9')
            then price else 0 end) as RENGA_Volume,
            sum(case when nft_address in ('0x394e3d3044fc89fcdd966d3cb35ac0b32b0cda91','0x64ad353bc90a04361c4810ae7b3701f3beb48d7e','0x5bd815fd6c096bab38b4c6553cfce3585194dff9')
            then price else 0 end)/sum(price) as Renga_percent
            from ethereum.core.ez_nft_sales
            where currency_symbol in ('WETH','ETH') and price_usd < 500000 and platform_name = 'opensea'
            and day > '2022-03-01 00:00:00.000'
            group by 1
            """
top = f"""
    SELECT 
    project_name,
    max(price) as price
    FROM ethereum.core.ez_nft_sales 
    where currency_symbol in ('WETH','ETH') 
    and total_fees_usd > 5 
    and platform_name = 'opensea'
    and date_trunc('day', block_timestamp) = current_date
    group by 1
    order by 2 desc
    limit 10
"""



# %%
query_result_set = sdk.query(sql)
query_result_set2 = sdk.query(top)


# %%
df = pd.DataFrame(query_result_set.records)
df
df2 = pd.DataFrame(query_result_set2.records)
df2

# %%
st.title('Opensea Volume')
##st.map(sql)
#st.line_chart(df, x='nft_address', y='mint_price_eth')
#st.line_chart(df, x='day', y='renga_percent')
#st.dataframe(sql)


chart = alt.Chart(df).mark_area(
    line={'color':'darkgreen'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='lightgreen', offset=0),
               alt.GradientStop(color='darkgreen', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    alt.X('day:T'),
    alt.Y('renga_percent:Q')
)

st.altair_chart(chart)

chart2 = alt.Chart(df2).mark_bar().encode(
    x='project_name',
    y='price')

st.altair_chart(chart2)
