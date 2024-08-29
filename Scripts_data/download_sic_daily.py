
import logging
logging.getLogger("copernicus_marine_root_logger").setLevel("ERROR")
import copernicusmarine as cm

cm.subset(motu_api_request = "python -m motuclient --motu https://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSISFORECAST_PHY_001_024-TDS --product-id cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m --longitude-min -167 --longitude-max -17 --latitude-min 14 --latitude-max 89.97 --date-min '1981-09-01 12:00:00' --date-max '2022-10-31 12:00:00'  --variable uo --variable vo --out-dir '/gpfs/fs7/eccc/cccs/hos000/SST_data/OSTIA_SICON' --out-name 'SICON_GLO_SST_L4_REP_OBSERVATIONS_1981_2022' --user hsankare --pwd 2023*Eharouna  --proxy-server=webproxy.science.gc.ca:8888/")
