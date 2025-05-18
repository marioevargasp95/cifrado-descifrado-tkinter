from dash import Dash, dcc, html, Input, Output, callback,dash_table,ctx
import os
import pandas as pd
from utils import create_datatable,extract_sentiments,get_wordcloud,create_avg_radar_plot
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_mantine_components as dmc
from io import StringIO


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
#
server = app.server
df=pd.read_csv('pqrs_updated.csv') # archivo fuente de datos principal
print(df['Periodo'].unique())
#print(df.columns)
# revisar por que algunas pqrs no tienen sede, seguramente porque con el correo no xruza, pero ..por qué?
df=df[df['sede'].isin(['VIRTUAL', 'META', 'BOGOTÁ','ESCUELA DE FORMACIÓN EMPRESARIAL'])]

with open('reference_dictionary.json','r') as jsonfile:# diccionario de sentimientos de Compensar
    new_dict=json.load(jsonfile)

df['Categoria']=df['Categoria'].fillna('Sin categoría')
categories=list(df['Categoria'].unique())
periods=sorted(list(df['Periodo'].unique()))

faculties=list(df[~df['facultad'].isnull()]['facultad'].unique())
sedes=list(df['sede'].unique())

df=df.rename(columns={'Sentimiento principal':'Sent ppal',\
                     'Sentimiento secundario':'Sent sec',\
                     'Polaridad sentimiento principal':'Polaridad 1',\
                     'Polaridad sentimiento secundario':'Polaridad 2'})
                     
########### Diseño de Layout########
# estilos para cada objeto
main_style={'display':'flex','width':'100%','height':'100%'}
dropdow_style_cat={'width':'90%','margin-left':'3%','margin-top':'10%'}
dropdow_style_period={'width':'90%','margin-left':'3%','margin-top':'20%'}
dropdow_style_sede={'width':'90%','margin-left':'3%','margin-top':'10%'}
dropdow_style_faculty={'width':'90%','margin-left':'3%','margin-top':'10%'}
dropdow_style_program={'width':'90%','margin-left':'3%','margin-top':'10%'}
checkbox_style={'width':'90%','margin-left':'5%','margin-top':'10%'}
side_menu_style={
    'background': '#FF7518',
    
    'width':'25%',
    'height':'2000px'    
}
main_content_style={'height':'700px','width':'80%'}
image_style={'margin-left':'18%','margin-top':'3%'}
title_style={'margin-left':'20%'}
wordcloud_style1={"width":"100%"}
wordcloud_style2={"width":"100%"}
counter_style={'width':'90%','margin-left':'4%','margin-top':'20%'}
cell_style_center = {'textAlign': 'center', 'verticalAlign': 'middle'}
# esta es el layout para la pagina general
general_item=dcc.Loading(id='loading1',children=[

                        html.Table([
                                    html.Tr([
                                        html.Td(html.H3('Nube de palabras general'),style=cell_style_center),
                                        html.Td(html.H3('Nube de palabras clave'),style=cell_style_center)
                                        
                                    ]),
                                    html.Tr([
                                        html.Td(html.Img(id='general-word-cloud', style=wordcloud_style1)),
                                        html.Td(html.Img(id='sent-word-cloud', style=wordcloud_style2))
                                    ]),
                                 
                                 
                                 ],style={'margin-left':'10%'}
                                 ),
                                   
                        html.Div([
                            html.Div(id='profile-IA-div',style={'flex':'1','width':'50%'}),
                            html.Div(id='pond-pol-div',style={'flex':'1','width':'50%'})
                        ],style={'display':'flex','flexDirection':'row'}),               
                        html.Div(id='general-charts-div-principal'),      
                    
                        html.Div(id='general-charts-div-secondary')

                                    
                    ])
# layout para comentarios individuales
individual_item= html.Div([
                            html.H2('Individual',style=title_style),
                            html.Div(id='individual-charts',children=['graficas individuales']),
                            dcc.Loading(id='Loading2',children=[
                                html.Div(id='comments-table-div',children=['Tabla de comentarios'])
                            ])

                        ])
# layout para graficas temporales
temp_item=html.Div([
                            html.H2('Temporal',style=title_style),
                            dcc.Loading(id='loading3',children=[
                                html.Div(id='temp-polarities'),
                                #html.Div(id='temp-princ-sents'),
                                html.Div(id='temp-factor-scores')
                            ])
                            


                  ])
# layout de acordeon para la segemntacion de sentimientos por Polaridades
sub_acc1_html=html.Div([
    html.H3('Sentimientos'),
    html.Div(id='positives-plot'),
    html.Div(id='negatives-plot'),


])
# layout de acordeon para la segmentacio de factores institucionales
sub_acc2_html=html.Div([
    html.H3('Factores Institucionales'),
    html.Div(id='factor-area-plot-pos'),
    html.Div(id='factor-area-plot-neg'),


])
#layouts de acordeon
sub_acc1=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Sentimientos'),
                    dmc.AccordionPanel(sub_acc1_html)
                ],value='Sub1')
sub_acc2=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Factores Institucionales'),
                    dmc.AccordionPanel(sub_acc2_html)
                ],value='Sub2')

# layout contenedor de factores sociodemograficos con la definición principal de acordeones
join_item=html.Div([
                         html.H3('factores sociodemográficos'),
                         dcc.Dropdown(id='demo-factors',
                                options=[
                                    {'label':'Semestre','value':'ubicacionSemestral'},
                                    {'label':'Género','value':'sexo'},
                                    {'label':'Edad','value':'age_group'},
                                    {'label':'Facultad','value':'facultad'},
                                    {'label':'Sede','value':'sede'},
                                    {'label':'NSE','value':'estrato'},

                            ],value='age_group'),
                         dcc.Loading(id='loading4',children=[

                            
                            dmc.MantineProvider(
                                dmc.Accordion(
                                    children=[
                                        sub_acc1,
                                        sub_acc2
                                    
                                    
                                ]
                                )
                            )


                         ])

                    ])
# menu acordeón General       
acc1=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Análisis general para el área seleccionada '),
                    dmc.AccordionPanel(general_item)
                ],value='General')
# menu acordeón Individual                
acc2=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Análisis por solicitud individual del área seleccionada'),
                    dmc.AccordionPanel(individual_item)
                ],value='Individual')
# menu acordeón Temporal
acc3=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Gráficas temporales'),
                    dmc.AccordionPanel(temp_item)
                ],value='Temporal')
# menu acordeon visión general
acc4=dmc.AccordionItem(
                [
                    dmc.AccordionControl('Segmentacion conjunta por factores institucionales'),
                    dmc.AccordionPanel(join_item)
                ],value='Conjunta')

# layout principal
app.layout =dmc.MantineProvider( html.Div([

    html.Div(id='main-container',children=[
        html.Div(id='menu-layout-div',children=[
            html.Img(src='assets/logo-ucompensar-2022.jpg',height=200,width=200,style=image_style),
            dcc.Dropdown(id='period',options=[{'label':i,'value':i} for i in periods],value='2024-2',style=dropdow_style_period),
            dcc.Dropdown(id='categories',options=[{'label':i,'value':i} for i in categories],value='Apoyo Financiero',style=dropdow_style_cat),
            dcc.Dropdown(id='sede',placeholder='Sede',multi=True,options=[{'label':i,'value':i} for i in sedes],style=dropdow_style_sede),
            dcc.Dropdown(id='faculty',placeholder='Facultad',multi=True,options=[{'label':i,'value':i} for i in faculties],style=dropdow_style_faculty),
            dcc.Dropdown(id='program',placeholder='Programa',multi=True,style=dropdow_style_program),
            dcc.Checklist(id='alert-selector',options=[{'label':'Casos con posible alerta','value':'yes'}],style=checkbox_style),
            dcc.Loading(id='loader3',children=[html.H3(id='requests-counter',children='cuenta',style=counter_style)]),
            dcc.Loading(id='loader4',children=[html.H3(id='verbatim-per',children='verbatim',style=counter_style)])
            ],
            style=side_menu_style
        ),
        html.Div(id='content-div',children=[
            
            html.H2('Análisis de sentimiento de casos en salesforce',style=title_style),
            dmc.Accordion(id='main-accordion',children=[
                acc1,
                acc4,
                acc2,
                acc3
                ]
            )
            #General
            

            #Individual

        
           

            ],style=main_content_style
        )


    ],style=main_style),
    dcc.Store(id='individual-store')

])
)
#######Fin diseño de Layout####


############Callbacks de manejos de eventos############
# en este callback se llenan los programas de acuerdo a la facultad
@app.callback(Output('program','options'),
             [Input('faculty','value')])
def fill_programs(faculty):
    if faculty is None:
        faculty=[]
    #print(faculty)
    if len(faculty)==0:
        programs_gen=list(df[~df['cicloCurricular'].isnull()]['cicloCurricular'].unique())
        options=[{'label':i,'value':i} for i in programs_gen]
    else:
        programs=list(df[(~df['cicloCurricular'].isnull())&(df['facultad'].isin(faculty))]['cicloCurricular'].unique())
        options=[{'label':i,'value':i} for i in programs]
    return options


# en este callback se publica la información relacionada con la pestaña pública
@app.callback(Output('comments-table-div','children'),
              Output('individual-store','data'),
              Output('general-charts-div-principal','children'),
              Output('general-charts-div-secondary','children'),
              Output('general-word-cloud','src'),
              Output('sent-word-cloud','src'),
              Output('requests-counter','children'),
              Output('profile-IA-div','children'),
              Output('temp-polarities','children'),
              #Output('temp-princ-sents','children'),
              Output('temp-factor-scores','children'),
              Output('positives-plot','children'),
              Output('negatives-plot','children'),
              Output('factor-area-plot-pos','children'),
              Output('factor-area-plot-neg','children'),
              Output('verbatim-per','children'),
              Output('pond-pol-div','children'),
              [Input('categories','value'),
              Input('period','value'),
              Input('sede','value'),
              Input('faculty','value'),
              Input('program','value'),
              Input('alert-selector','value'),
              Input('demo-factors','value')])
def show_comments(category,period,sede,facultad,programa,alert,demofactors):
    cols=['Id. del caso','NombreCompleto','facultad','sede','cicloCurricular','dia','Propietario del caso','Descripcion','Sent ppal','Polaridad 1',\
    'Sent sec','Polaridad 2','pond_pol']
    #print(demofactors)
    if facultad is None:
        facultad=[]
    if sede is None:
        sede=[]
    if programa is None:
        programa=[]

    #print(category, period)
    # aqui se hacen los filtros del usuario
    if category is  None and period is None:
        filtered=df
    elif category is  not None and period is None:
        filtered=df[df['Categoria']==category]
    elif category is None and period is not None:
        filtered=df[df['Periodo']==period]
    else:
        filtered=df[(df['Periodo']==period)&((df['Categoria']==category))]
    
    if len(sede)>0:
        filtered=filtered[filtered['sede'].isin(sede)]
    
    if len(facultad)>0:
        filtered=filtered[filtered['facultad'].isin(facultad)]
   
    if len(programa)>0:
        filtered=filtered[filtered['cicloCurricular'].isin(programa)]
    if alert is None:
        alert=[]
    if len(alert)>0:
        if alert[0]=='yes':
            filtered=filtered[filtered['Alerta']=='Alerta']



    
    # sentimiento principal
    fig = make_subplots(
        rows=1, cols=2,  # 1 row and 2 columns
        column_widths=[0.5, 0.5],  # Adjust column widths if needed
        subplot_titles=("Sentimientos principales", "Polaridad principal"),
        specs=[[{"type": "bar"}, {"type": "pie"}]]  # Specify types of subplots
        )
    
    sent_counter=filtered['Sent ppal'].value_counts()
    
    pol_pie=filtered['Polaridad 1'].value_counts().sort_index()
    barfig=go.Bar(x=sent_counter.index,y=sent_counter.values,marker=dict(color='orange'),name='Sentimientos')
    piefig=go.Pie(labels=pol_pie.index,values=pol_pie.values,marker=dict(colors=['#FF474C','#023E8A']))
    fig.add_trace(barfig,row=1,col=1)
    fig.add_trace(piefig,row=1,col=2)
    fig.update_layout(height=400)
    principal_figure=dcc.Graph(figure=fig)
    # sentimiento secundario
    fig2 = make_subplots(
        rows=1, cols=2,  # 1 row and 2 columns
        column_widths=[0.5, 0.5],  # Adjust column widths if needed
        subplot_titles=("Sentimientos secundarios", "Polaridad secundaria"),
        specs=[[{"type": "bar"}, {"type": "pie"}]]  # Specify types of subplots
        )
    
    sent_counter2=filtered['Sent sec'].value_counts()
    
    pol_pie2=filtered['Polaridad 2'].value_counts().sort_index()
    barfig2=go.Bar(x=sent_counter2.index,y=sent_counter2.values,marker=dict(color='green'),name='Sentimientos')
    piefig2=go.Pie(labels=pol_pie2.index,values=pol_pie2.values,marker=dict(colors=['#FF474C','#023E8A']))
    fig2.add_trace(barfig2,row=1,col=1)
    fig2.add_trace(piefig2,row=1,col=2)
    fig2.update_layout(height=400)
    secondary_figure=dcc.Graph(figure=fig2)

    #wordcloud
    wordcloud_df=filtered[~filtered['clean_des'].isnull()]
    verbatim=round(100*filtered[~filtered['Sent ppal'].isnull()].shape[0]/filtered.shape[0],2)
    verbatim =f'Verbatim: {verbatim}%'
    text=' '.join(list(wordcloud_df['clean_des'].values))
    if len(text.strip())>0:
        img_object=get_wordcloud(text)
    else:
        img_object=''
    #sentiments cloud
    wordcloud_sent_df=filtered[~filtered['Descripcion'].isnull()]
    destext=' '.join(list(wordcloud_sent_df['Descripcion'].values))

    sentiments,_=extract_sentiments(destext,new_dict)
    sent_l=[k for s in sentiments for k in s]
    text2=' '.join(sent_l)
    if len(text2.strip()):
        img_sent=get_wordcloud(text2)
    else:
        img_sent=''
    # factors profile

    factors_fig=dcc.Graph(id='gen-profile-IA',figure=create_avg_radar_plot(filtered))

    count=wordcloud_df.shape[0]
    msg=f'Total casos: {count}'

    #polarity temporal plot
    pol_groupdf=filtered.groupby(['dia','Polaridad 1']).count()[['Id. del caso']].reset_index()
    #print(sent_groupdf.head())
    temp_pol_fig=px.bar(pol_groupdf,x='dia',y='Id. del caso',color='Polaridad 1',color_discrete_sequence=['red','blue','gray'])
    temp_pol_fig.update_yaxes(title='Casos')
    temp_pol_fig.update_layout(title='Polaridad en función del tiempo')
    temp_pol_chart=dcc.Graph(figure=temp_pol_fig)
    #sentiment temporal plot
    #sent_groupdf=filtered.groupby(['dia','Sent ppal']).count()[['Id. del caso']].reset_index()
    #sent_fig=px.bar(sent_groupdf,x='dia',y='Id. del caso',color='Sent ppal')
    #sent_fig.update_layout(title='Sentimientos en función del tiempo')
    #sent_fig.update_yaxes(title='Casos')
    #sent_chart=dcc.Graph(figure=sent_fig)
    
    #factors temporal plot
    
    factors_group_df=filtered.groupby('dia').mean(numeric_only=True)[['socioeconomico','academico','institucional','individual']].reset_index()
    factors_plot=go.Figure()
    for f in ['socioeconomico','academico','institucional','individual']:
        factors_plot.add_trace(go.Scatter(x=factors_group_df['dia'],y=factors_group_df[f].rolling(window=7).mean(),name=f))
    factors_plot.update_yaxes(title='Promedio')
    factors_plot.update_layout(title='Puntaje promedio de factores en el tiempo')
    factors_chart=dcc.Graph(figure=factors_plot)

    #histograma normalizado
    factors_list_demo={'ubicacionSemestral': 'Semestre',
                        'sexo': 'Género',
                        'age_group': 'Edad',
                        'facultad': 'Facultad',
                        'sede': 'Sede',
                        'estrato': 'NSE'}
    #
    #age_ordered_factors=['15-19',
    #                    '20-24',
    #                    '25-29',
    #                    '30-34',
    #                    '35-39',
    #                   '40-44',
    #                    '45-49',
    #                    '50-54',
    #                    '55-59',
    #                    '60-64',
    #                    '65+']
    
    hist_norm=filtered.groupby([demofactors,'Polaridad 1','Sent ppal']).count()[['Id. del caso']].reset_index()
    hist_norm_neg=hist_norm[hist_norm['Polaridad 1']=='Negativa']
    hist_norm_pos=hist_norm[hist_norm['Polaridad 1']=='Positiva']
    
    ordered_factors=sorted(filtered[~filtered[demofactors].isnull()][demofactors].unique())
    fig_neg=px.histogram(hist_norm_neg,x=demofactors,y='Id. del caso',color='Sent ppal', barnorm='percent',
                        text_auto=True,color_discrete_sequence=px.colors.qualitative.Set1,
                        category_orders={demofactors:ordered_factors})
    sum_hist_norm_neg=hist_norm_neg.groupby([demofactors]).sum().reset_index()
    #print(sum_hist_norm_neg)
    for x1,x2 in zip(sum_hist_norm_neg[demofactors],sum_hist_norm_neg['Id. del caso']):
        fig_neg.add_annotation(x=x1,y=110,text=f'{x2} Casos', showarrow=False,)
    fig_neg.update_yaxes(title='Porcentaje de casos')
    fig_neg.update_xaxes(title=factors_list_demo[demofactors],type='category')
    fig_neg.update_layout(bargap=0.02,title='Polaridad Negativa',title_x=0.5)
    fig_neg.update_traces(texttemplate='%{y:.2f}%')
    
    
    fig_pos=px.histogram(hist_norm_pos,x=demofactors,y='Id. del caso',color='Sent ppal', barnorm='percent',
                        text_auto=True,color_discrete_sequence=px.colors.qualitative.D3,
                        category_orders={demofactors:ordered_factors}
                        )
    sum_hist_norm_pos=hist_norm_pos.groupby([demofactors]).sum().reset_index()
    for x1,x2 in zip(sum_hist_norm_pos[demofactors],sum_hist_norm_pos['Id. del caso']):
        fig_pos.add_annotation(x=x1,y=110,text=f'{x2} Casos', showarrow=False,)
    fig_pos.update_layout(bargap=0.02,title='Polaridad Positiva',title_x=0.5)
    fig_pos.update_traces(texttemplate='%{y:.2f}%')
    fig_pos.update_yaxes(title='Porcentaje de casos')
    fig_pos.update_xaxes(title=factors_list_demo[demofactors],type='category')
    neg_chart=dcc.Graph(figure=fig_neg)
    pos_chart=dcc.Graph(figure=fig_pos)

    # factores ministerio segun factores institucionales
    factor_grouped=filtered.groupby([demofactors,'Polaridad 1']).mean(numeric_only=True)[['institucional','individual','academico','socioeconomico']].reset_index()
    factor_grouped_neg=factor_grouped[factor_grouped['Polaridad 1']=='Negativa']
    factor_grouped_pos=factor_grouped[factor_grouped['Polaridad 1']=='Positiva']
    area_fig_pos=go.Figure()
    for ifac in ['institucional','individual','academico','socioeconomico']:
        area_fig_pos.add_trace(go.Scatter(x=factor_grouped_pos[demofactors],y=factor_grouped_pos[ifac],name=ifac,stackgroup='one'))
        #area_fig_pos.add_trace(go.Bar(x=factor_grouped_pos[demofactors],y=factor_grouped_pos[ifac],name=ifac))
    area_fig_pos.update_xaxes(type='category',title=factors_list_demo[demofactors])
    area_fig_pos.update_yaxes(title='Puntaje')
    area_fig_pos.update_layout(title='Polariad Positiva',title_x=0.5,barmode='stack')
    area_chart_pos=dcc.Graph(figure=area_fig_pos)

    area_fig_neg=go.Figure()
    for ifac in ['institucional','individual','academico','socioeconomico']:
        area_fig_neg.add_trace(go.Scatter(x=factor_grouped_neg[demofactors],y=factor_grouped_neg[ifac],name=ifac,stackgroup='one'))
    area_fig_neg.update_xaxes(type='category',title=factors_list_demo[demofactors])
    area_fig_neg.update_yaxes(title='Puntaje')
    area_fig_neg.update_layout(title='Polariad Negativa',title_x=0.5)
    area_chart_neg=dcc.Graph(figure=area_fig_neg)

    #pond_pol
    pond_pol_count=filtered['pond_pol'].value_counts()
    pond_pol_count=pd.DataFrame(pond_pol_count).reset_index()
    pond_pol_fig=px.pie(pond_pol_count,values='count',
        names='pond_pol',
        color='pond_pol',
        color_discrete_map={
            'Negativa': '#FF4433',
            'Positiva': '#4040FF',
            'Neutra': 'gray'
        }
    )
    pond_pol_fig.update_layout(title='Polaridad ponderada')
    pond_pol_chart=dcc.Graph(figure=pond_pol_fig)



    


    # se removió sent_chart
    return create_datatable(filtered[cols]),filtered.to_json(),principal_figure,secondary_figure,\
            img_object,img_sent,msg,factors_fig,temp_pol_chart,factors_chart,pos_chart,neg_chart,area_chart_pos,area_chart_neg,verbatim,\
            pond_pol_chart

# en este callback se publica la información relacionada con la pestaña individual
@app.callback(Output('individual-charts','children'),
            [Input('comments-table','selected_rows'),
             Input('individual-store','data')])
def show_individual(row,individual_data):
    
    try:
        #new_df=pd.read_json(individual_data).reset_index()
        new_df=pd.read_json(StringIO(individual_data)).reset_index()
        factores=['Socieconómico','Individual','Académico','Institucional']
        description=new_df.loc[row,'Descripcion'].values[0]
        soc_factor=new_df.loc[row,'socioeconomico'].values[0]
        ind_factor=new_df.loc[row,'individual'].values[0]
        inst_factor=new_df.loc[row,'institucional'].values[0]
        acad_factor=new_df.loc[row,'academico'].values[0]

        #print('socio',soc_factor)
        #print('ind',ind_factor)
        #print('inst',inst_factor)
        #print('acad',acad_factor)
        rev_list,pond_df=extract_sentiments(description,new_dict)
        fig = make_subplots(
            rows=1, cols=3,  # 1 row and 2 columns
            column_widths=[0.5, 0.3,0.5],  # Adjust column widths if needed
            subplot_titles=("Sentimientos", "",""),
            specs=[[{"type": "bar"}, {"type": "table"}, {"type": "polar"}]]  # Specify types of subplots
        )
        
        tablefig=go.Table(header=dict(values=['Comentario']),cells=dict(values=[description]))
        print(pond_df)
        barfig=go.Bar(x=pond_df['sentiments'].values,y=pond_df['count'].values,name='Sentimientos')
        polarfig=go.Scatterpolar(r=[soc_factor,ind_factor,acad_factor,inst_factor],theta=factores,fill='toself',name='Factores Ministerio')
        fig.add_trace(barfig,row=1,col=1)
        fig.add_trace(tablefig,row=1,col=2)
        fig.add_trace(polarfig,row=1,col=3)


        final_figure=dcc.Graph(figure=fig)

        return final_figure

    except Exception as e: 
        print(e)
    return ''



if __name__ == '__main__':
    #app.run(debug=True,host='108.61.166.45')
    app.run(host='172.21.7.111',debug=True)
