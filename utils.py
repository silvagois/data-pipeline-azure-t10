# Imports

import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import pytz
from azure.storage.blob import BlobServiceClient

columns_convert_int = ['quantidade','aliquota_icms']
data_types_nfe = {
      'codigo_produto' : np.int64,
      'descricao_produto' : object,                 
      'ncm' : object,
      'valor' : np.float64,
      'quantidade' : np.float64,
      'base_calculo_icms': np.float64,
      'aliquota_icms' : np.float64,
      'valor_icms' : np.float64,
      'codigo_uf_emitente' : np.int64,
      'codigo_nf' : np.int64,
      'numero_nf' : np.int64,
      'data_emissao' : np.datetime64,
      'natureza_operacao' : object ,
      'cnpj_emitente' : object,
      'nome_emitente' : object,
      'logadouro_emitente' : object,
      'numero_emitente' : object,
      'bairro_emitente' : object,
      'fone_emitente' : object,
      'nome_cliente' : object      
   }

# FUNÇÕES GLOBAIS
def read_context(json_path: str):
    """
    Read json content in order to get context variables from data process.
    Args:
        json_path: path from where json file containing project
            information is.
    """

    context_file = open(json_path)
    context = json.load(context_file)

    return context

def set_dtypes(df, dtypes):
    for column in dtypes:
        #print(column)
        df[column] = df[column].astype(dtypes[column])
    return df

def convert_float_to_int(df, columns):
    for column in columns:
        df[column] = df[column].astype(np.int64)
    return df

def data_load():
    brasil_fuso_horario = pytz.timezone("America/Sao_Paulo")
    data_atual = datetime.now(brasil_fuso_horario).strftime("%Y-%m-%d %H:%M:%S")
    return data_atual

def cria_data_fonte_e_carga(df,coluna):
    df['data_fonte'] = pd.to_datetime(df[coluna], format='%Y-%m-%d %H:%M:%S',errors='ignore').dt.strftime('%Y-%m-%d %H:%M')
    df['data_carga']  = data_load()
    return df

def cria_coluna_year_month_day(df,coluna: str):
    df["year"] = df[coluna].str.slice(0,4)
    df["month"] = df[coluna].str.slice(5,7)
    df["day"] = df[coluna].str.slice(8,10)
    return df

def connect_storage_account():
    context = read_context('context/transform-info.json')
    connect_str = context['transform-info'][0]['connect_string']
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def get_container_xml_raw(container : str, blob : str):
    blob_service_client = connect_storage_account()
    raw_container_client = blob_service_client.get_container_client(container)

    # Especificando o caminho do arquivo CSV no seu bucket
    blob_client = raw_container_client.get_blob_client(blob)

    # Lendo o arquivo CSV em um objeto pandas DataFrame
    #csv_data = blob_client.download_blob().content_as_text()
    xml = blob_client.download_blob()
    return xml

def create_data_frame_danfe(xml):
    # define o namespace
    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    # carrega o arquivo XML
    tree = ET.parse(xml)
    root = tree.getroot()

    # extrai os dados das tags
    cUF = root.find('.//nfe:cUF', namespace).text
    cNF = root.find('.//nfe:cNF', namespace).text
    numero_nf = root.find('.//nfe:nNF', namespace).text
    data_emissao = root.find('.//nfe:dhEmi', namespace).text
    natOp = root.find('.//nfe:natOp', namespace).text
    CNPJ_emit = root.find('.//nfe:CNPJ', namespace).text
    nome_emitente = root.find('.//nfe:emit/nfe:xNome', namespace).text
    logadouro_emitente = root.find('.//nfe:emit/nfe:enderEmit/nfe:xLgr', namespace).text
    numero_emitente = root.find('.//nfe:emit/nfe:enderEmit/nfe:nro', namespace).text
    bairro_emitente  = root.find('.//nfe:emit/nfe:enderEmit/nfe:xBairro', namespace).text
    fone_emitente  = root.find('.//nfe:emit/nfe:enderEmit/nfe:fone', namespace).text
    nome_cliente = root.find('.//nfe:dest/nfe:xNome', namespace).text

    # cria o DataFrame com as colunas desejadas
    df = pd.DataFrame(columns=['codigo_produto', 'descricao_produto', 'ncm', 'valor', 'quantidade','base_calculo_icms','aliquota_icms','valor_icms'])

    # itera sobre todas as tags <det> para extrair os dados de cada produto
    for det in root.findall('.//nfe:det', namespace):
        prod_dict = {
            'codigo_produto': det.find('nfe:prod/nfe:cProd', namespace).text,
            'descricao_produto': det.find('nfe:prod/nfe:xProd', namespace).text,
            'ncm': det.find('nfe:prod/nfe:NCM', namespace).text,
            'valor': det.find('nfe:prod/nfe:vProd', namespace).text,
            'quantidade': det.find('nfe:prod/nfe:qCom', namespace).text,
            'base_calculo_icms' : det.find('nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:vBC', namespace).text,
            'aliquota_icms' : det.find('nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:pICMS', namespace).text,
            'valor_icms' : det.find('nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:vICMS', namespace).text

        }
        
        # adiciona o dicionário ao DataFrame
        df = df.append(prod_dict, ignore_index=True)
        df['codigo_uf_emitente'] = cUF
        df['codigo_nf'] = cNF
        df['numero_nf'] = numero_nf
        df['data_emissao'] = data_emissao
        df['natureza_operacao'] = natOp
        df['cnpj_emitente'] = CNPJ_emit
        df['nome_emitente'] = nome_emitente
        df['logadouro_emitente'] = logadouro_emitente
        df['numero_emitente'] = numero_emitente       
        df['bairro_emitente'] = bairro_emitente       
        df['fone_emitente'] = fone_emitente         
        df['nome_cliente'] = nome_cliente
        return df
    
def save_container_processing_parquet(df,blob_service_client):
    # SAve parquet processing .get_blob_client('danfe.parquet')
    processing_container_name = blob_service_client.get_container_client("processing")
    parquet_blob_client = blob_service_client.get_container_client(processing_container_name).get_blob_client('danfe.parquet')
    parquet_blob_data = df.to_parquet(parquet_blob_client, partition_cols=['year', 'month', 'day'], index=False, engine='fastparquet')
    parquet_blob_client.upload_blob(parquet_blob_data, overwrite=True)