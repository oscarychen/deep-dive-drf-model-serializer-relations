# All About Django REST Framework Model Serializer

---
_Advanced use cases for Django REST Framework Model Serializers_

## Part I: The basics

In Part I, we are going to set up a few Django models for us to play with, and then set up a couple of REST APIs using
ModelSerializers; nothing special going on here if you are already familiar with how to use DRF generic views.
![image](docs/carmaker_erd.png)

In the center of our ERD, the `VehicleModel` model has the following relations:

- One-to-one relation with `Project`
- Many-to-one (foreign key) relation with `Manufacturer`
- Many-to-one (foreign key) relation with `VehicleModel` (itself)
- Many-to-many relation with `Engine`

As well as the following Django reverse relations:

- Many-to-one (foreign key) relation from `Vehicle`
- Many-to-many relation from `Engineer`

See [carmaker.models](carmaker/models.py) for details on the model set up.

For this part, I've also set up a couple of views using Django REST Framework generic views with ModelSerializers.
Because I want to expand on the APIs later, I'm putting the APIs in Part I in their own module called [api_1](api_1).

With a standard `ModelSerializer` for `VehicleModel` such as:

```python
class VehicleModelSerializer(ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"
```

and a standard `ListCreateAPIView`:

```python
class VehicleModelListCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
```

We can start testing these APIs.

### Default Read Behavior

We can now call the listing endpoint using:

```commandline
curl --location --request GET 'http://localhost:8000/api_1/'
```

and get the following response:

```json
[
  {
    "id": 1,
    "model": "Buick D-35 Roadster",
    "year": 1917,
    "project": 1,
    "maker": 1,
    "predecessor": null,
    "engine_options": [
      1,
      2
    ]
  }
]
```

We can make the following observations about DRF `ModelSerializer`'s default **read** behavior:

- Returns Django model attributes as they are defined on ORM model, including auto fields
- Returns value of appropriate type as defined by the ORM model field
- Includes all relations declared on the ORM model
- The related instances are returned as their primary keys
- Does not include any Django reverse relations

### Default Write Behavior

Similarly, we can call the same endpoint to create a new instance:

```commandline
curl --location --request POST 'http://localhost:8000/api_1/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "model": "Buick D-35 Roadster 2",
        "year": 1919,
        "project": null,
        "maker": 1,
        "predecessor": 1,
        "engine_options": [
            1,
            2
        ]
    }'
```

You can play around with this request data, and try to include some additional related fields, and make the following
observation about DRF `ModelSerializer`'s default **write** behavior:

- Relations can be made using existing related instance primary key
- Django reverse relations are ignored
- Unrecognized and read-only attributes are ignored

---

## Part II: Include related instance data

Part II example code can be found in module [api_2](api_2).

A common way of including related instance data is through nesting of the serializers:

```python
class VehicleModelSerializer(ModelSerializer):
    project = ProjectSerializer()
    maker = ManufacturerSerializer()
    engine_options = EngineSerializer(many=True)
    vehicle_set = VehicleSerializer(many=True)  # reverse relation 'vehicle_set'
    engineers_responsible = EngineerSerializer(many=True, source="engineer_set.all")  # reverse relation 'engineer_set'

    class Meta:
        model = VehicleModel
        fields = "__all__"
```

### Reading with related instance data

With this serializer, we can hit the listing endpoint again. Note that the reverse relations will even work as
long as the reverse attribute name declared on the serializer matches what is on the ORM model, or
initialized with the `source` argument pointing to a matching ORM model attribute.
You should see the response data containing a list of objects like the following:

```json
{
  "id": 1,
  "project": {
    "id": 1,
    "code_name": "project-d-35-roadster"
  },
  "maker": {
    "id": 1,
    "name": "Buick"
  },
  "engine_options": [
    {
      "id": 1,
      "name": "Model D Inline-4",
      "displacement": 2.7
    },
    {
      "id": 2,
      "name": "Chevrolet Inline-4",
      "displacement": 2.8
    }
  ],
  "vehicle_set": [
    {
      "id": 1,
      "VIN": "A123456789",
      "model": 1
    }
  ],
  "engineers_responsible": [
    {
      "id": 1,
      "name": "Yoshida",
      "works_on": [
        1
      ]
    }
  ],
  "model": "Buick D-35 Roadster",
  "year": 1917,
  "predecessor": null
}
```

A couple of takeaways:

- Related instance nested serializer must be initialized with `many=True` if there are more than one instance expected
- Reverse relation also works

### Writing related instance data

I think creating and updating related instance is probably a bad RESTful design, but sometimes we may be asked to do so
because the related model may be very small.

Interestingly, if we try to call the creation endpoint, the API still expects only the primary keys for constructing
relations, the behavior is exactly the same as the serializer from Part I even though we specified serializers for
related instances. The reverse relation data is still being ignored.

In the next part, we will talk about how to design a serializer that can handle touching related instance data.

Takeaways:

- Related model data is only referred to using primary key even if a nested serializer is used
- Django reverse relations are still ignored in write operation

---

## Part III: Hoisting related model data

To be continued..