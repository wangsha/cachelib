import time

import pytest
from clear import ClearTests
from common import CommonTests
from has import HasTests

from cachelib.mongodb import MongoDbCache


@pytest.fixture(autouse=True, params=[MongoDbCache])
def cache_factory(request):
    def _factory(self, *args, **kwargs):
        kwargs["db"] = "test-db"
        kwargs["collection"] = "test-collection"
        kwargs["key_prefix"] = "prefix"

        rc = request.param(*args, **kwargs)
        index_info = rc.client.index_information()
        all_keys = {
            subkey[0] for value in index_info.values() for subkey in value["key"]
        }
        assert "id" in all_keys, "Failed to create index on 'id' field"
        assert "expiration" in all_keys, "Failed to create index on 'expiration' field"
        rc.clear()
        return rc

    if request.cls:
        request.cls.cache_factory = _factory


class TestMongoDbCache(CommonTests, ClearTests, HasTests):
    def test_auto_expire(self):
        """Test that MongoDB's TTL index automatically expires cache entries."""
        cache = self.cache_factory()
        # Set a cache entry with a short timeout
        cache.set("auto_expire_key", "value", timeout=2)

        # Verify it exists
        assert cache.get("auto_expire_key") == "value"

        # Wait for expiration (add buffer time for MongoDB TTL monitor)
        time.sleep(5)

        # Verify it has expired
        assert cache.get("auto_expire_key") is None
