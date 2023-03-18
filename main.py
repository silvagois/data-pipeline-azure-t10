from utils import *

def main ():
    blob_service_client = connect_storage_account()
    xml = get_container_xml_raw('raw','cobase-nfe2.xml')
    df = create_data_frame_danfe(xml)
    df = set_dtypes(df, data_types_nfe)
    df = convert_float_to_int(df,columns_convert_int)
    df = cria_data_fonte_e_carga(df, 'data_emissao')
    df = cria_coluna_year_month_day(df, 'data_fonte')    
    #save_container_processing_parquet(df,blob_service_client)

if __name__ == "__main__":
    main()