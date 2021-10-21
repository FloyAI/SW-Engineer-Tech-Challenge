import asyncio
import unittest
from threading import Thread
from unittest import IsolatedAsyncioTestCase
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

from client import SeriesDispatcher
from mocks.mock_scu import mock_scu


# https://realpython.com/testing-third-party-apis-with-mock-servers/

class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(requests.codes.ok)
        self.end_headers()
        return

class SeriesDispatchTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_server = HTTPServer(('localhost', 8000), MockServerRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

        self.engine = SeriesDispatcher()

    # async def asyncSetUp(self):
    #     self.engine = SeriesDispatcher()
    #     await self.engine.main()
        # self.engine.loop = asyncio.get_event_loop()
        # self.engine.loop.run_until_complete(self.engine.main())
        # Thread(
        #     self.engine.loop.run_until_complete(self.engine.main()),
        #     daemon=True
        # )

    def test_sending_series(self):
        scu_response = mock_scu()
        print(scu_response)
        self.assertEqual(scu_response, 'C-STORE request status: 0x0000')

if __name__ == "__main__":
    unittest.main()
