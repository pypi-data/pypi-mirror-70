import unittest

from imputena import random_value_imputation

from test.example_data import *


class TestRandomValueImputation(unittest.TestCase):

    # Positive tests for data as a dataframe ----------------------------------

    def test_RVI_df_returning(self):
        """
        Positive test

        data: Correct dataframe (divcols)

        Checks that the original dataframe remains unmodified and that the
        returned dataframe contains 0 NA values, 18 less than the original.
        """
        # 1. Arrange
        df = generate_example_df_divcols()
        # 2. Act
        df2 = random_value_imputation(df)
        # 3. Assert
        self.assertEqual(df.isna().sum().sum(), 18)
        self.assertEqual(df2.isna().sum().sum(), 0)

    def test_RVI_df_inplace(self):
        """
        Positive test

        data: Correct dataframe (divcols)

        Checks that random_value_interpolation removes 18 values from the
        dataframe.
        """
        # 1. Arrange
        df = generate_example_df_divcols()
        # 2. Act
        random_value_imputation(df, inplace=True)
        # 3. Assert
        self.assertEqual(df.isna().sum().sum(), 0)

    def test_RVI_df_normal_distribution(self):
        """
        Positive test

        data: Correct dataframe (divcols)
        distribution: 'normal'

        Checks that the original dataframe remains unmodified and that the
        returned dataframe contains 0 NA values, 18 less than the original.
        """
        # 1. Arrange
        df = generate_example_df_divcols()
        # 2. Act
        df2 = random_value_imputation(df, 'normal')
        # 3. Assert
        self.assertEqual(df.isna().sum().sum(), 18)
        self.assertEqual(df2.isna().sum().sum(), 0)

    def test_RVI_df_integer_distribution(self):
        """
        Positive test

        data: Correct dataframe (divcols)
        distribution: 'integer'

        Checks that the original dataframe remains unmodified and that the
        returned dataframe contains 0 NA values, 18 less than the original.
        """
        # 1. Arrange
        df = generate_example_df_divcols()
        # 2. Act
        df2 = random_value_imputation(df, 'integer')
        # 3. Assert
        self.assertEqual(df.isna().sum().sum(), 18)
        self.assertEqual(df2.isna().sum().sum(), 0)

    # Positive tests for data as a series -------------------------------------

    def test_RVI_series_returning(self):
        """
        Positive test

        data: Correct series (example series)

        Checks that the original series remains unmodified and that the
        returned dataframe contains 0 NA values, 3 less than the original.
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act
        ser2 = random_value_imputation(ser)
        # 3. Assert
        self.assertEqual(ser.isna().sum().sum(), 3)
        self.assertEqual(ser2.isna().sum().sum(), 0)

    def test_RVI_series_inplace(self):
        """
        Positive test

        data: Correct series (example series)

        Checks that random_value_interpolation removes 3 NA values from the
        series.
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act
        random_value_imputation(ser, inplace=True)
        # 3. Assert
        self.assertEqual(ser.isna().sum().sum(), 0)

    def test_RVI_series_normal_distribution(self):
        """
        Positive test

        data: Correct series (example series)
        distribution: 'normal'

        Checks that the original series remains unmodified and that the
        returned dataframe contains 0 NA values, 3 less than the original.
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act
        ser2 = random_value_imputation(ser, 'normal')
        # 3. Assert
        self.assertEqual(ser.isna().sum().sum(), 3)
        self.assertEqual(ser2.isna().sum().sum(), 0)

    def test_RVI_series_integer_distribution(self):
        """
        Positive test

        data: Correct series (example series)
        distribution: 'integer'

        Checks that the original series remains unmodified and that the
        returned dataframe contains 0 NA values, 3 less than the original.
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act
        ser2 = random_value_imputation(ser, 'integer')
        # 3. Assert
        self.assertEqual(ser.isna().sum().sum(), 3)
        self.assertEqual(ser2.isna().sum().sum(), 0)

    # Negative tests ----------------------------------------------------------

    def test_RVI_wrong_type(self):
        """
        Negative test

        data: array (unsupported type)

        Checks that the function raises a TypeError if the data is passed as
        an array.
        """
        # 1. Arrange
        data = [2, 4, np.nan, 1]
        # 2. Act & 3. Assert
        with self.assertRaises(TypeError):
            random_value_imputation(data)

    def test_RVI_df_wrong_columns(self):
        """
        Negative test

        data: Correct dataframe (divcols)
        columns: ['z'] ('z' doesn't exist as a column in the data)

        Checks that random_value_interpolation raises a ValueError if one of
        the specified columns doesn't exist in the data.
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act & Assert
        with self.assertRaises(ValueError):
            random_value_imputation(ser, columns=['z'])

    def test_RVI_df_invalid_distribution(self):
        """
        Negative test

        data: Correct dataframe (divcols)
        distribution: '' (invalid value)

        Checks that random_value_interpolation raises a ValueError when an
        unrecognized distribution is passed
        """
        # 1. Arrange
        ser = generate_example_series()
        # 2. Act & Assert
        with self.assertRaises(ValueError):
            random_value_imputation(ser, '')
