import unittest

from question import FundraiserError, FundraiserPool, count_matches


class GenerateCodeTests(unittest.TestCase):
    def test_generate_code_00000(self):
        pool = FundraiserPool(random_source=lambda: 0.0)
        self.assertEqual(pool._generate_code(), "00000")

    def test_generate_code_99999(self):
        pool = FundraiserPool(random_source=lambda: 0.999999)
        self.assertEqual(pool._generate_code(), "99999")

    def test_generate_code_55555(self):
        # An interior value that isolates this case from endpoint bugs.
        pool = FundraiserPool(random_source=lambda: 0.555559)
        self.assertEqual(pool._generate_code(), "55555")


class EntryTests(unittest.TestCase):
    def test_enter_after_draw_raises_without_changing_state(self):
        pool = FundraiserPool(random_source=lambda: 0.5)
        pool.enter("Mina")
        draw = pool.close_draw()
        pot_before = pool.pot_cents
        entries_before = tuple(draw.entries)

        with self.assertRaises(FundraiserError):
            pool.enter("Julio")

        self.assertEqual(pool.pot_cents, pot_before)
        self.assertEqual(tuple(draw.entries), entries_before)


class CountMatchesTests(unittest.TestCase):
    def test_same_digits_in_different_order_only_count_matching_positions(self):
        # Only the middle digit (3) is in the same position.
        self.assertEqual(count_matches("12345", "54321"), 1)


if __name__ == "__main__":
    unittest.main()
