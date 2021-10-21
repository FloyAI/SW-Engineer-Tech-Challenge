# SW-Engineer-Tech-Challenge
Hello and welcome to our software challenge, we're glad to have you here 👋

Right away, **a note on how to work on and submit the challenge**: Please fork this repository using the Fork button in the upper right on the repository start site.
You can work on the challenge in your fork then (more detailed information is provided in the challenge description linked above).
For submission, it is not necessary to create a pull request.

This repository contains template code and sample data that you can use during the challenge.
The description of the challenge, which contains all information you should need to solve the challenge, can be found here: [Challenge description](https://floyai.atlassian.net/wiki/external/84377616/NmZjYjZkZmJkYTcxNGNlMDgyODQ0OWUzYWYxNjZhY2I?atlOrigin=eyJpIjoiNTg3N2E0NTVhMjBlNDVmM2I1NGNiNmVmOWMwZGRiZmEiLCJwIjoiYyJ9).

We recommend you to read this document carefully.
If we update this document during the challenge, we will inform you about this separately.


We with you a lot of fun and success with the challenge 🚀

# NOTES
- Packages are needed to run tests and server. Run `pip install -r requirements.txt` to install them
- `pytest` is used to run the tests
- `uvicorn api.main:app --reload` to start the server
- `python client.py` to start the client
- `sudo docker run -p 4242:4242 -p 8042:8042 -p 6667 --add-host=host.docker.internal:host-gateway floyai_1` to start the PACS
- Tests are of an end-to-end type but are incomplete. The test for clients specifically does not touch the functions because more time is needed to become conversant with testing asyncio functions.
- Negative Tests for the server have also not been included for the same reason above.
