import apache_beam as beam

# Counting all unique elements
with beam.Pipeline() as pipeline:
  total_unique_elements = (
      pipeline
      | 'Create produce' >> beam.Create(
          ['🍓', '🥕', '🥕', '🥕', '🍆', '🍆', '🍅', '🍅', '🍅', '🌽'])
      | 'Count unique elements' >> beam.combiners.Count.PerElement()
      | beam.Map(print))


if __name__ == "__main__":
    print("The total count is displayed above")