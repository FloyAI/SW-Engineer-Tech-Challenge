import time
import asyncio
from copy import deepcopy

from pydicom import Dataset
from scp import ModalityStoreSCP

# docker exec -it <container_id> /bin/bash
# /etc/orthanc/orthanc.json
# sudo docker run -p 4242:4242 -p 8042:8042 -p 6667 --add-host=host.docker.internal:host-gateway floyai_1

class SeriesCollector:
    """A Series Collector is used to build up a list of instances (a DICOM series) as they are received by the modality.
    It stores the (during collection incomplete) series, the Series (Instance) UID, the time the series was last updated
    with a new instance and the information whether the dispatch of the series was started.
    """
    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset (instance).

        Args:
            first_dataset (Dataset): The first dataset or the regarding series received from the modality.
        """
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        """Add an dataset to the series collected by this Series Collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset to add.

        Returns:
            bool: `True`, if the Series UID of the dataset to add matched and the dataset was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True

        return False


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplyfication, you can assume that only one series is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher.
        """

        self.loop: asyncio.AbstractEventLoop
        self.modality_scp = ModalityStoreSCP()
        self.series_collector = None

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether or not datasets are received from the modality and prints a message
        regulary when no datasets are received.
        """
        self.series_collector = {}
        while True:
            if self.modality_scp.Series.items():
                for series_id, instances_ in self.modality_scp.Series.items():
                    try:
                        if len(self.series_collector[series_id]) < 5:
                            self.series_collector[series_id].append(len(instances_))
                        else:
                            self.series_collector[series_id].pop(0)
                            self.series_collector[series_id].append(len(instances_))
                    except KeyError:
                        self.series_collector[series_id] = [len(instances_)]
                
                for series_id, instance_lens in deepcopy(self.series_collector).items():
                    # latest 5 values should be similar to qualify as all datasets having been collected
                    if len(instance_lens) == 5 and instance_lens[0] == instance_lens[-1]:
                        await self.dispatch_series_collector(series_id)
                        del self.modality_scp.Series[series_id]
                        del self.series_collector[series_id]

                print("collecting series:", self.series_collector)

            await asyncio.sleep(0.2)

    async def dispatch_series_collector(self, series_id) -> None:
        series_instance = self.modality_scp.Series[series_id][0]
        series_ = {
                "SeriesInstanceUID": series_instance.SeriesInstanceUID,
                "PatientName": series_instance.PatientName,
                "PatientID": series_instance.PatientID,
                "StudyInstanceUID": series_instance.StudyInstanceUID,
                "InstancesInSeries": len(self.modality_scp.Series[series_id])
            }
        print(series_)


if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())
