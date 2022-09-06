import asyncio
import time
from pydicom import Dataset
from scp import ModalityStoreSCP


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
        print(f"Created series collector for id {self.series_instance_uid}")

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
            print(f"Added to series {self.series_instance_uid} at {self.last_update_time}")
            return True

        return False


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplification, you can assume that only one series is transmitted at a time.
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
        regularly when no datasets are received.
        """
        while True:
            # Check for new datasets and collect them into series
            if self.modality_scp.datasets_to_store:
                print(f"{len(self.modality_scp.datasets_to_store)} datasets to store!")

                collect_datasets = asyncio.create_task(self.run_series_collectors())
                await collect_datasets

            # Attempt to dispatch any series which are ready
            if self.series_collector:
                await self.dispatch_series_collector()
            
            print("Waiting for Modality")
            await asyncio.sleep(0.2)

    async def run_series_collectors(self) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled.
        """
        for dataset in list(self.modality_scp.datasets_to_store):
            if self.series_collector:
                self.series_collector.add_instance(dataset)

            else:
                self.series_collector = SeriesCollector(dataset)

            # delete first entry in original `datasets_to_store` each time we process a dataset
            # should allow appending to end of the list (receiving new events) while processing
            del self.modality_scp.datasets_to_store[0]

    async def dispatch_series_collector(self) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the series collector hasn't had an update for a long enough timespan and send the series to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server
        maximum_wait_time = 1

        if time.time() - self.series_collector.last_update_time > maximum_wait_time:
            print("no more updates, safe to dispatch")
            self.series_collector.dispatch_started = True

            # start dispatching


if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())
