from models import Tcu,TcuData
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy.orm import Session

class Usina(object):
    def __init__(self, Session: Session):
        self._session = Session()

    def get_tcus(self) -> list[dict]:
        """ 
        Retorna lista de TCUs da Usina
        """
        tcus = self._session.query(Tcu).filter(Tcu.active == True).all()
        data = [tcu.get_attr_dict() for tcu in tcus]
        return data

    def get_tcu_uplinks(self, id: str, n_uplinks: int) -> list[dict]:
        """
        Retorna os n_uplinks mais recentes de uma TCU
        """
        uplinks = self._session.query(TcuData).filter(TcuData.tcu_id == id).order_by(TcuData.datetime.desc()).limit(n_uplinks).all()
        data = [uplink.get_attr_dict() for uplink in uplinks]
        return data

    def get_plant_summary(self) -> list[dict]:
        """Retorna o último uplink de cada TCU
        """
        tcus = self.get_tcus()
        data = []
        for tcu in tcus:
            uplinks = self.get_tcu_uplinks(tcu["id"], 1)  
            if uplinks: 
                data.append(uplinks[0]) 
        return data
