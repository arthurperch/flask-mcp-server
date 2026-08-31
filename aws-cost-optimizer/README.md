# AWS Cost Optimizer (lab dashboard)

A Flask page that lists a few AWS resources and estimated spend.

It is a lab. It does not use machine learning, and it is not a FinOps product.

## Run it

```bash
cd aws-cost-optimizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

Needs AWS credentials with read access to the services it lists.
