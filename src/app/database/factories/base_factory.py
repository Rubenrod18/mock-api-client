import factory
from faker import Faker

faker = Faker()


class BaseFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def build_dict(cls, exclude: set = None, **kwargs):
        """Builds a dictionary representation of the factory instance.

        Args
        ----
            exclude: set
                List of field names to exclude.
            kwargs:
                Additional fields to override.

        Returns
        -------
            dict:
                The dictionary representation of the factory instance.
        """
        exclude_fields = set(exclude or [])
        instance = cls.build(**kwargs)
        return {
            field: getattr(instance, field) for field in cls._meta.declarations.keys() if field not in exclude_fields
        }
