#!/bin/bash
gunicorn -w 3 server:app
