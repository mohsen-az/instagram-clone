from django.test import TestCase

from location.models import Location


class LocationModelTestCase(TestCase):
    def setUp(self) -> None:
        self.location = Location(
            title="Tehran",
            points={"lat": 32.543, "long": "332.545"}
        )

    def test_location_model_representation(self):
        self.assertEqual(self.location.__str__(), self.location.title)
