from utils import LDD_CONNECTOR as CONNECTOR
import pandas as pd


class EWIC:
    def __init__(self, start_date: str, end_date: str):
        self.CONNECTOR = CONNECTOR
        self.start_date = start_date
        self.end_date = end_date

    def df_ampere(self) -> pd.DataFrame:
        ampere_query_str = f"""
            SELECT A.date_time, A.value AS Ampere, A_t.name
            FROM pgcbfinal.east_west_interconnector_amp_reading AS A 
            JOIN pgcbfinal.east_west_interconnector_amp_type AS A_t ON A.connector_id = A_t.id
            WHERE A.date_time BETWEEN '{self.start_date}' AND '{self.end_date}'
            """
        df_ampere = pd.read_sql(ampere_query_str, CONNECTOR, index_col=['date_time'])
        return df_ampere

    def df_mw(self) -> pd.DataFrame:
        mw_query_str = f"""
            SELECT t.id, t.name, mw.value, mw.date_time FROM 
            pgcbfinal.east_west_interconnector_mw AS mw 
            JOIN pgcbfinal.east_west_interconnector_mw_mv_type AS t ON mw.connector_id = t.id
            WHERE mw.date_time BETWEEN '{self.start_date}' AND '{self.end_date}'
        """
        # df_mw = pd.read_sql(mw_query_str, CONNECTOR, index_col=['date_time', 'id'])
        df_mw = pd.read_sql(mw_query_str, CONNECTOR, index_col=None)
        return df_mw

    def df_energy_reading(self) -> pd.DataFrame:
        energy_reading_query_str = f"""
                    SELECT l.id, l.name, r.date, r.value, l.multiplication_factor FROM
                    pgcbfinal.east_west_interconnector_line_reading AS r 
                    JOIN pgcbfinal.east_west_interconnector_line AS l ON r.line_id = l.id
                    WHERE r.date BETWEEN '{self.start_date}' AND '{self.end_date}'
                """
        df_energy_reading = pd.read_sql(energy_reading_query_str, CONNECTOR, index_col=None)
        return df_energy_reading

    def df_ampere_mw_fomatted(self) -> pd.DataFrame:
        df_mw_formatted = self.df_mw().pivot(index='date_time', columns='name', values='value')
        df_ampere_mw = df_mw_formatted.join(df_ampere)
        return df_ampere_mw


ewic = EWIC(start_date='2022-7-1', end_date='2022-7-31 23:00')
df_ampere = ewic.df_ampere()
df_mw = ewic.df_mw()
df_reading = ewic.df_energy_reading()
b = ewic.df_ampere_mw_fomatted()
a = 5
