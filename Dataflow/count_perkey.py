import apache_beam as beam

# Counting elements for each key
with beam.Pipeline() as pipeline:
  total_elements_per_keys = (
      pipeline
      | 'Create plants' >> beam.Create([
          ('spring', '🍓'),
          ('spring', '🥕'),
          ('summer', '🥕'),
          ('fall', '🥕'),
          ('spring', '🍆'),
          ('winter', '🍆'),
          ('spring', '🍅'),
          ('summer', '🍅'),
          ('fall', '🍅'),
          ('summer', '🌽'),
      ])
      | 'Count elements per key' >> beam.combiners.Count.PerKey()
      | beam.Map(print))


if __name__ == "__main__":
    print("The total count is displayed above")