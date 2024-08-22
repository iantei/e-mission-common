import unittest

import emcommon.metrics.footprint.egrid as emcmfe

KG_PER_LB = 0.453592

# eGRID expected values (collected from https://www.epa.gov/egrid/data-explorer)
# "I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
# at the <eGRID subregion> level for <2022>."
EGRID_EXPECTED_LBS_PER_KWH = {
    'RFCW': 1005.90,
    'NWPP': 605.87,
}


class TestEgrid(unittest.IsolatedAsyncioTestCase):
    async def test_egrid_intensity_cincinnati_2022(self):
        # Cincinnati, OH (RFCW region)
        coords = [-84.52, 39.13]
        (kg_per_kwh, metadata) = await emcmfe.get_egrid_intensity_for_coords(2022, coords)

        expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["RFCW"] * KG_PER_LB
        expected_metadata = {
            "data_sources": ["egrid2022"],
            "data_source_urls": [
                "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
            ],
            "is_provisional": False,
            "requested_year": 2022,
            "requested_coords": coords,
            "egrid_region": "RFCW",
        }
        self.assertAlmostEqual(kg_per_kwh, expected_kg_per_kwh, places=2)
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])

    async def test_egrid_intensity_eagle_point_2023(self):
        # Eagle Point, OR (NWPP region)
        coords = [-122.83, 42.29]
        (kg_per_kwh, metadata) = await emcmfe.get_egrid_intensity_for_coords(2023, coords)

        expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["NWPP"] * KG_PER_LB
        expected_metadata = {
            "data_sources": ["egrid2022"],
            "data_source_urls": [
                "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
            ],
            "is_provisional": True,  # provisional; 2023 was requested but 2022 was used
            "requested_year": 2023,
            "requested_coords": coords,
            "egrid_region": "NWPP",
        }
        self.assertAlmostEqual(kg_per_kwh, expected_kg_per_kwh, places=2)
        for key in expected_metadata:
            self.assertEqual(metadata[key], expected_metadata[key])
