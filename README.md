Purpose : Unveil is a platform built with the intention to help developers showcase their talent and make recruitment easier for recruiters by providing them with means to handle an entire cycle of recruitment process at a single place and developers to apply to a job as smoothly as possible.

To run in local:
backend:

cd backend
pip3 install -r requirements.txt
uvicorn src.main:app --reload

** make sure to use python 3.11

frontend:
cd frontend
npm install
npm run dev