from pydicom.dataset import FileMetaDataset
from pynetdicom import AE, events, evt, debug_logger
from pynetdicom.sop_class import MRImageStorage

# debug_logger()


class ModalityStoreSCP():
    def __init__(self) -> None:
        self.ae = AE(ae_title=b'STORESCP')
        self.scp = None
        self.Series = {}
        self._configure_ae()

    def _configure_ae(self) -> None:
        """Configure the Application Entity with the presentation context(s) which should be supported and start the SCP server.
        """
        handlers = [(evt.EVT_C_STORE, self.handle_store)]

        self.ae.add_supported_context(MRImageStorage)
        self.scp = self.ae.start_server(('0.0.0.0', 6667), block=False, evt_handlers=handlers)
        print("SCP Server started")

    def handle_store(self, event: events.Event) -> int:
        """Callable handler function used to handle a C-STORE event.

        Args:
            event (Event): Representation of a C-STORE event.

        Returns:
            int: Status Code
        """
        dataset = event.dataset
        dataset.file_meta = FileMetaDataset(event.file_meta)
        if dataset.SeriesInstanceUID not in self.Series.keys():
            self.Series[dataset.SeriesInstanceUID] = [dataset]
        else:
            self.Series[dataset.SeriesInstanceUID].append(dataset)

        return 0x0000
