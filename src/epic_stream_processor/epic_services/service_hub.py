from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import Dict
from typing import List

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
# from geoalchemy2 import Geometry
from pytz import utc  # type: ignore[import]
from sqlalchemy.engine import Engine
#from streamz import Stream


from ..epic_orm.pg_pixel_storage import Database


T = TypeVar("T")


class ServiceHub:
    # _pg_conn = None
    # _pg_engine = create_engine("postgresql:///postgres?host=/var/run/postgresql")

    def __init__(self, engine: Engine | None = None) -> None:
        """connect to ectd and and also have a scheduler from apscheduler"""
        self._scheduler = BackgroundScheduler(timezone=utc)
        #self._pipeline = Stream(stream_name="service_hub")
        self._scheduler.start()
        self._pgdb: Database
        self._connect_pgdb(engine)
        self._epic_instances = []

        # define the stream processor timed_window(5)
        # IMPORTANT: If using a timed window, never set the window to 0!
        # self._pipeline.map(ServiceHub.detect_transient).timed_window(5).sink(
        #     self.insert_multi_epoch_pgdb
        # )

    def __call__(self, *args, **kwargs) -> ServiceHub:  # type: ignore[no-untyped-def]
        if not hasattr(self, "instance"):
            self.instance: ServiceHub = super().__call__(*args, **kwargs)  # type: ignore[misc]
        return self.instance

    def _connect_pgdb(self, engine: Engine | None = None) -> None:
        # establish postgres connection
        # TODO: fetch the connection details from sys config service

        self._pgdb = Database(engine=engine, create_all_tables=False)
        try:
            print()
            # self._pg_conn = psycopg.connect(
            #     dbname="postgres", user="batman", host="/var/run/postgresql"
            # )
            # self._pg_conn.autocommit = True
            # print("Postgres connection established")
        except Exception as e:
            print(e)
            print("Retrying connection in 60 seconds")
            self.schedule_job_delay(self._connect_pgdb, None, 60)

    def insert_single_epoch_pgdb(
        self,
        pixel_df: pd.DataFrame,
        pixel_meta_df: pd.DataFrame,
    ) -> None:
        self._pipeline.emit(dict(pixels=pixel_df, meta=pixel_meta_df))

    @staticmethod
    def detect_transient(upstream: object) -> object:
        return upstream

    def insert_multi_epoch_pgdb(
        self,
        upstream: (
            list[dict[pd.DataFrame, pd.DataFrame]] | dict[pd.DataFrame, pd.DataFrame]
        ),
    ) -> None:
        pixels_df = []
        metadata_df = []

        if type(upstream) == dict:
            upstream = [upstream]

        if len(upstream) < 1:
            return

        for i in upstream:
            # print("inloop")
            # print(i)
            # print("after p")
            pixels_df.append(i["pixels"])
            metadata_df.append(i["meta"])

        pixels_df_merged = pd.concat(pixels_df)
        metadata_df_merged = pd.concat(metadata_df)

        pixels_df_merged.to_sql(
            "epic_pixels",
            con=self._pgdb._engine,
            dtype=dict(pixel_skypos=Geometry(geometry_type="POINT", srid=4326)),
            if_exists="append",
            index=False,
        )

        metadata_df_merged.to_sql(
            "epic_img_metadata",
            con=self._pgdb._engine,
            if_exists="append",
            index=False,
        )

    # def pg_query(self, query: str, args: tuple[Any, ...] | None = None) -> list[Any]:
    #     if self._pg_conn is None:
    #         raise (ConnectionRefusedError("Could not establish connection to the pgdb"))
    #     else:
    #         result = []
    #         result = self._pg_conn.execute(query, args).fetchall()
    #         return result
    def get_num_epic_instances(self):
        count = 0
        dead_instances = []
        for i, inst in enumerate(self._epic_instances):
            if inst["process"] is not None and inst["process"].poll() is None:
                count += 1
            else:
                dead_instances.append(i)

        for i in dead_instances:
            del self._epic_instances[i]

        return count

    def get_epic_instances(self) -> List[Dict[str, str]]:
        instances = []
        dead_instances = []
        for i, inst in enumerate(self._epic_instances):
            if inst["process"] is not None and inst["process"].poll() is None:
                instances.append(dict(options=inst["options"], pid=inst["process"].pid))
            else:
                dead_instances.append(i)

        for i in dead_instances:
            del self._epic_instances[i]

        return instances

    def add_epic_instance(self, inst: Dict[str, object]):
        self._epic_instances.append(inst)

    def schedule_job_delay(
        self,
        func: Callable[..., Any],
        args: tuple[Any, ...] | None = None,
        seconds: int | float = 604800,
    ) -> None:
        self._scheduler.add_job(
            func,
            trigger="date",
            args=args,
            run_date=datetime.now() + timedelta(seconds),
        )

    def schedule_job_date(
        self,
        func: Callable[..., Any],
        timestamp: datetime,
        args: tuple[Any, ...] | None = None,
    ) -> None:
        self._scheduler.add_job(func, trigger="date", args=args, run_date=timestamp)
