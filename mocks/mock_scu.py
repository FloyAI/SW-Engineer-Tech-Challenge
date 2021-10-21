from pydicom import dcmread

from pynetdicom import AE
from pynetdicom.sop_class import MRImageStorage

# https://pydicom.github.io/pynetdicom/stable/examples/storage.html

def mock_scu():
    # Initialise the Application Entity
    ae = AE()

    # Add a requested presentation context
    ae.add_requested_context(MRImageStorage)

    # Read in our DICOM CT dataset
    ds = dcmread('sample_data/0001/SE000001/1_0000.dcm')

    # Associate with peer AE at IP 127.0.0.1 and port 6667
    assoc = ae.associate('127.0.0.1', 6667)
    if assoc.is_established:
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)

        # Check the status of the storage request
        if status:
            # If the storage request succeeded this will be 0x0000
            print(f'C-STORE request status: 0x{0:04x}'.format(status.Status))
            return f'C-STORE request status: 0x{0:04x}'.format(status.Status)
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')

if __name__ == "__main__":
    mock_scu()