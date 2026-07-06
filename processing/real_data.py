REAL_SOURCE_TYPES = {'officielle', 'media', 'terrain', 'interne'}
SIMULATION_SOURCE_TYPES = {'simulation', 'synthetique', 'synthétique'}
SIMULATION_SOURCE_NAMES = {'donnee experimentale', 'donnée expérimentale'}


def _normalized(value):
    return str(value or '').strip().lower()


def is_real_source(source_type, source_name=None):
    normalized_type = _normalized(source_type)
    normalized_name = _normalized(source_name)
    return (
        normalized_type in REAL_SOURCE_TYPES
        and normalized_type not in SIMULATION_SOURCE_TYPES
        and normalized_name not in SIMULATION_SOURCE_NAMES
    )


def real_data_mask(df):
    source_type = df.get('source_type')
    if source_type is None:
        return df.index == df.index

    source_name = df.get('source_name')
    if source_name is None:
        source_name = ''

    return source_type.combine(source_name, is_real_source)


def keep_real_data(df):
    return df.loc[real_data_mask(df)].copy()
