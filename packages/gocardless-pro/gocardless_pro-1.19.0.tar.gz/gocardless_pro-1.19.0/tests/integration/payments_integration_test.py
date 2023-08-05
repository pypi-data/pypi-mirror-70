# WARNING: Do not edit by hand, this file was generated by Crank:
#
#   https://github.com/gocardless/crank
#

import json

import requests
import responses
from nose.tools import (
  assert_equal,
  assert_is_instance,
  assert_is_none,
  assert_is_not_none,
  assert_not_equal,
  assert_raises
)

from gocardless_pro.errors import MalformedResponseError
from gocardless_pro import resources
from gocardless_pro import list_response

from .. import helpers
  

@responses.activate
def test_payments_create():
    fixture = helpers.load_fixture('payments')['create']
    helpers.stub_response(fixture)
    response = helpers.client.payments.create(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
    assert_is_not_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal(response.amount, body.get('amount'))
    assert_equal(response.amount_refunded, body.get('amount_refunded'))
    assert_equal(response.charge_date, body.get('charge_date'))
    assert_equal(response.created_at, body.get('created_at'))
    assert_equal(response.currency, body.get('currency'))
    assert_equal(response.description, body.get('description'))
    assert_equal(response.id, body.get('id'))
    assert_equal(response.metadata, body.get('metadata'))
    assert_equal(response.reference, body.get('reference'))
    assert_equal(response.retry_if_possible, body.get('retry_if_possible'))
    assert_equal(response.status, body.get('status'))
    assert_equal(response.fx.estimated_exchange_rate,
                 body.get('fx')['estimated_exchange_rate'])
    assert_equal(response.fx.exchange_rate,
                 body.get('fx')['exchange_rate'])
    assert_equal(response.fx.fx_amount,
                 body.get('fx')['fx_amount'])
    assert_equal(response.fx.fx_currency,
                 body.get('fx')['fx_currency'])
    assert_equal(response.links.creditor,
                 body.get('links')['creditor'])
    assert_equal(response.links.instalment_schedule,
                 body.get('links')['instalment_schedule'])
    assert_equal(response.links.mandate,
                 body.get('links')['mandate'])
    assert_equal(response.links.payout,
                 body.get('links')['payout'])
    assert_equal(response.links.subscription,
                 body.get('links')['subscription'])

@responses.activate
def test_payments_create_new_idempotency_key_for_each_call():
    fixture = helpers.load_fixture('payments')['create']
    helpers.stub_response(fixture)
    helpers.client.payments.create(*fixture['url_params'])
    helpers.client.payments.create(*fixture['url_params'])
    assert_not_equal(responses.calls[0].request.headers.get('Idempotency-Key'),
                     responses.calls[1].request.headers.get('Idempotency-Key'))

def test_timeout_payments_create_idempotency_conflict():
    create_fixture = helpers.load_fixture('payments')['create']
    get_fixture = helpers.load_fixture('payments')['get']
    with helpers.stub_timeout_then_idempotency_conflict(create_fixture, get_fixture) as rsps:
      response = helpers.client.payments.create(*create_fixture['url_params'])
      assert_equal(2, len(rsps.calls))

    assert_is_instance(response, resources.Payment)

@responses.activate
def test_timeout_payments_create_retries():
    fixture = helpers.load_fixture('payments')['create']
    with helpers.stub_timeout_then_response(fixture) as rsps:
      response = helpers.client.payments.create(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)

def test_502_payments_create_retries():
    fixture = helpers.load_fixture('payments')['create']
    with helpers.stub_502_then_response(fixture) as rsps:
      response = helpers.client.payments.create(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
  

@responses.activate
def test_payments_list():
    fixture = helpers.load_fixture('payments')['list']
    helpers.stub_response(fixture)
    response = helpers.client.payments.list(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, list_response.ListResponse)
    assert_is_instance(response.records[0], resources.Payment)

    assert_equal(response.before, fixture['body']['meta']['cursors']['before'])
    assert_equal(response.after, fixture['body']['meta']['cursors']['after'])
    assert_is_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal([r.amount for r in response.records],
                 [b.get('amount') for b in body])
    assert_equal([r.amount_refunded for r in response.records],
                 [b.get('amount_refunded') for b in body])
    assert_equal([r.charge_date for r in response.records],
                 [b.get('charge_date') for b in body])
    assert_equal([r.created_at for r in response.records],
                 [b.get('created_at') for b in body])
    assert_equal([r.currency for r in response.records],
                 [b.get('currency') for b in body])
    assert_equal([r.description for r in response.records],
                 [b.get('description') for b in body])
    assert_equal([r.id for r in response.records],
                 [b.get('id') for b in body])
    assert_equal([r.metadata for r in response.records],
                 [b.get('metadata') for b in body])
    assert_equal([r.reference for r in response.records],
                 [b.get('reference') for b in body])
    assert_equal([r.retry_if_possible for r in response.records],
                 [b.get('retry_if_possible') for b in body])
    assert_equal([r.status for r in response.records],
                 [b.get('status') for b in body])

@responses.activate
def test_timeout_payments_list_retries():
    fixture = helpers.load_fixture('payments')['list']
    with helpers.stub_timeout_then_response(fixture) as rsps:
      response = helpers.client.payments.list(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, list_response.ListResponse)
    assert_is_instance(response.records[0], resources.Payment)

    assert_equal(response.before, fixture['body']['meta']['cursors']['before'])
    assert_equal(response.after, fixture['body']['meta']['cursors']['after'])

def test_502_payments_list_retries():
    fixture = helpers.load_fixture('payments')['list']
    with helpers.stub_502_then_response(fixture) as rsps:
      response = helpers.client.payments.list(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, list_response.ListResponse)
    assert_is_instance(response.records[0], resources.Payment)

    assert_equal(response.before, fixture['body']['meta']['cursors']['before'])
    assert_equal(response.after, fixture['body']['meta']['cursors']['after'])

@responses.activate
def test_payments_all():
    fixture = helpers.load_fixture('payments')['list']

    def callback(request):
        if 'after=123' in request.url:
          fixture['body']['meta']['cursors']['after'] = None
        else:
          fixture['body']['meta']['cursors']['after'] = '123'
        return [200, {}, json.dumps(fixture['body'])]

    url = 'http://example.com' + fixture['path_template']
    responses.add_callback(fixture['method'], url, callback)

    all_records = list(helpers.client.payments.all())
    assert_equal(len(all_records), len(fixture['body']['payments']) * 2)
    for record in all_records:
      assert_is_instance(record, resources.Payment)
    
  

@responses.activate
def test_payments_get():
    fixture = helpers.load_fixture('payments')['get']
    helpers.stub_response(fixture)
    response = helpers.client.payments.get(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
    assert_is_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal(response.amount, body.get('amount'))
    assert_equal(response.amount_refunded, body.get('amount_refunded'))
    assert_equal(response.charge_date, body.get('charge_date'))
    assert_equal(response.created_at, body.get('created_at'))
    assert_equal(response.currency, body.get('currency'))
    assert_equal(response.description, body.get('description'))
    assert_equal(response.id, body.get('id'))
    assert_equal(response.metadata, body.get('metadata'))
    assert_equal(response.reference, body.get('reference'))
    assert_equal(response.retry_if_possible, body.get('retry_if_possible'))
    assert_equal(response.status, body.get('status'))
    assert_equal(response.fx.estimated_exchange_rate,
                 body.get('fx')['estimated_exchange_rate'])
    assert_equal(response.fx.exchange_rate,
                 body.get('fx')['exchange_rate'])
    assert_equal(response.fx.fx_amount,
                 body.get('fx')['fx_amount'])
    assert_equal(response.fx.fx_currency,
                 body.get('fx')['fx_currency'])
    assert_equal(response.links.creditor,
                 body.get('links')['creditor'])
    assert_equal(response.links.instalment_schedule,
                 body.get('links')['instalment_schedule'])
    assert_equal(response.links.mandate,
                 body.get('links')['mandate'])
    assert_equal(response.links.payout,
                 body.get('links')['payout'])
    assert_equal(response.links.subscription,
                 body.get('links')['subscription'])

@responses.activate
def test_timeout_payments_get_retries():
    fixture = helpers.load_fixture('payments')['get']
    with helpers.stub_timeout_then_response(fixture) as rsps:
      response = helpers.client.payments.get(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)

def test_502_payments_get_retries():
    fixture = helpers.load_fixture('payments')['get']
    with helpers.stub_502_then_response(fixture) as rsps:
      response = helpers.client.payments.get(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
  

@responses.activate
def test_payments_update():
    fixture = helpers.load_fixture('payments')['update']
    helpers.stub_response(fixture)
    response = helpers.client.payments.update(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
    assert_is_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal(response.amount, body.get('amount'))
    assert_equal(response.amount_refunded, body.get('amount_refunded'))
    assert_equal(response.charge_date, body.get('charge_date'))
    assert_equal(response.created_at, body.get('created_at'))
    assert_equal(response.currency, body.get('currency'))
    assert_equal(response.description, body.get('description'))
    assert_equal(response.id, body.get('id'))
    assert_equal(response.metadata, body.get('metadata'))
    assert_equal(response.reference, body.get('reference'))
    assert_equal(response.retry_if_possible, body.get('retry_if_possible'))
    assert_equal(response.status, body.get('status'))
    assert_equal(response.fx.estimated_exchange_rate,
                 body.get('fx')['estimated_exchange_rate'])
    assert_equal(response.fx.exchange_rate,
                 body.get('fx')['exchange_rate'])
    assert_equal(response.fx.fx_amount,
                 body.get('fx')['fx_amount'])
    assert_equal(response.fx.fx_currency,
                 body.get('fx')['fx_currency'])
    assert_equal(response.links.creditor,
                 body.get('links')['creditor'])
    assert_equal(response.links.instalment_schedule,
                 body.get('links')['instalment_schedule'])
    assert_equal(response.links.mandate,
                 body.get('links')['mandate'])
    assert_equal(response.links.payout,
                 body.get('links')['payout'])
    assert_equal(response.links.subscription,
                 body.get('links')['subscription'])

@responses.activate
def test_timeout_payments_update_retries():
    fixture = helpers.load_fixture('payments')['update']
    with helpers.stub_timeout_then_response(fixture) as rsps:
      response = helpers.client.payments.update(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)

def test_502_payments_update_retries():
    fixture = helpers.load_fixture('payments')['update']
    with helpers.stub_502_then_response(fixture) as rsps:
      response = helpers.client.payments.update(*fixture['url_params'])
      assert_equal(2, len(rsps.calls))
      assert_equal(rsps.calls[0].request.headers.get('Idempotency-Key'),
                   rsps.calls[1].request.headers.get('Idempotency-Key'))
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
  

@responses.activate
def test_payments_cancel():
    fixture = helpers.load_fixture('payments')['cancel']
    helpers.stub_response(fixture)
    response = helpers.client.payments.cancel(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
    assert_is_not_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal(response.amount, body.get('amount'))
    assert_equal(response.amount_refunded, body.get('amount_refunded'))
    assert_equal(response.charge_date, body.get('charge_date'))
    assert_equal(response.created_at, body.get('created_at'))
    assert_equal(response.currency, body.get('currency'))
    assert_equal(response.description, body.get('description'))
    assert_equal(response.id, body.get('id'))
    assert_equal(response.metadata, body.get('metadata'))
    assert_equal(response.reference, body.get('reference'))
    assert_equal(response.retry_if_possible, body.get('retry_if_possible'))
    assert_equal(response.status, body.get('status'))
    assert_equal(response.fx.estimated_exchange_rate,
                 body.get('fx')['estimated_exchange_rate'])
    assert_equal(response.fx.exchange_rate,
                 body.get('fx')['exchange_rate'])
    assert_equal(response.fx.fx_amount,
                 body.get('fx')['fx_amount'])
    assert_equal(response.fx.fx_currency,
                 body.get('fx')['fx_currency'])
    assert_equal(response.links.creditor,
                 body.get('links')['creditor'])
    assert_equal(response.links.instalment_schedule,
                 body.get('links')['instalment_schedule'])
    assert_equal(response.links.mandate,
                 body.get('links')['mandate'])
    assert_equal(response.links.payout,
                 body.get('links')['payout'])
    assert_equal(response.links.subscription,
                 body.get('links')['subscription'])

def test_timeout_payments_cancel_doesnt_retry():
    fixture = helpers.load_fixture('payments')['cancel']
    with helpers.stub_timeout(fixture) as rsps:
      with assert_raises(requests.ConnectTimeout):
        response = helpers.client.payments.cancel(*fixture['url_params'])
      assert_equal(1, len(rsps.calls))

def test_502_payments_cancel_doesnt_retry():
    fixture = helpers.load_fixture('payments')['cancel']
    with helpers.stub_502(fixture) as rsps:
      with assert_raises(MalformedResponseError):
        response = helpers.client.payments.cancel(*fixture['url_params'])
      assert_equal(1, len(rsps.calls))
  

@responses.activate
def test_payments_retry():
    fixture = helpers.load_fixture('payments')['retry']
    helpers.stub_response(fixture)
    response = helpers.client.payments.retry(*fixture['url_params'])
    body = fixture['body']['payments']

    assert_is_instance(response, resources.Payment)
    assert_is_not_none(responses.calls[-1].request.headers.get('Idempotency-Key'))
    assert_equal(response.amount, body.get('amount'))
    assert_equal(response.amount_refunded, body.get('amount_refunded'))
    assert_equal(response.charge_date, body.get('charge_date'))
    assert_equal(response.created_at, body.get('created_at'))
    assert_equal(response.currency, body.get('currency'))
    assert_equal(response.description, body.get('description'))
    assert_equal(response.id, body.get('id'))
    assert_equal(response.metadata, body.get('metadata'))
    assert_equal(response.reference, body.get('reference'))
    assert_equal(response.retry_if_possible, body.get('retry_if_possible'))
    assert_equal(response.status, body.get('status'))
    assert_equal(response.fx.estimated_exchange_rate,
                 body.get('fx')['estimated_exchange_rate'])
    assert_equal(response.fx.exchange_rate,
                 body.get('fx')['exchange_rate'])
    assert_equal(response.fx.fx_amount,
                 body.get('fx')['fx_amount'])
    assert_equal(response.fx.fx_currency,
                 body.get('fx')['fx_currency'])
    assert_equal(response.links.creditor,
                 body.get('links')['creditor'])
    assert_equal(response.links.instalment_schedule,
                 body.get('links')['instalment_schedule'])
    assert_equal(response.links.mandate,
                 body.get('links')['mandate'])
    assert_equal(response.links.payout,
                 body.get('links')['payout'])
    assert_equal(response.links.subscription,
                 body.get('links')['subscription'])

def test_timeout_payments_retry_doesnt_retry():
    fixture = helpers.load_fixture('payments')['retry']
    with helpers.stub_timeout(fixture) as rsps:
      with assert_raises(requests.ConnectTimeout):
        response = helpers.client.payments.retry(*fixture['url_params'])
      assert_equal(1, len(rsps.calls))

def test_502_payments_retry_doesnt_retry():
    fixture = helpers.load_fixture('payments')['retry']
    with helpers.stub_502(fixture) as rsps:
      with assert_raises(MalformedResponseError):
        response = helpers.client.payments.retry(*fixture['url_params'])
      assert_equal(1, len(rsps.calls))
  
