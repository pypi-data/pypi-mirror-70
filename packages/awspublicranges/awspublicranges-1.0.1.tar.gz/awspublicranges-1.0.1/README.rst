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
