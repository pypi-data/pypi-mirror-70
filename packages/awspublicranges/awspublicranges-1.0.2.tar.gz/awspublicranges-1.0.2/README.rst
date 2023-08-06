Atlas API
==========

Small library to make grabbing an processing AWS public IP address ranges easier.


Usage
------

.. code:: python

    from awspublicranges.ranges import AwsIpRanges

    out = AwsIpRanges()

    for each_range in out.prefixes_for_lambda('us-west-2'):
        pprint(each_range.__dict__)


Master
------

.. image:: https://circleci.com/gh/mgmonteleone/python-atlasapi/tree/master.svg?style=svg&circle-token=34ce5f4745b141a0ee643bd212d85359c0594884
    :target: https://circleci.com/gh/mgmonteleone/python-atlasapi/tree/master