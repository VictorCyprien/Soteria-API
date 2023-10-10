from marshmallow import fields, Schema


class VendorGroupList(Schema):
    vendorGroupHash = fields.Integer(metadata={"description": "The hash of the vendor group"})
    vendorHashed = fields.List(fields.Integer(), metadata={"description": "The list of vendor's hash"})

    class Meta:
        ordered = True


class VendorDataGroup(Schema):
    groups = fields.Nested(
        VendorGroupList, 
        many=True,
        metadata={"description": "The list of vendors group"}
    )


class VendorGroups(Schema):
    data = fields.Nested(VendorDataGroup, metadata={"description": "The data of the vendor group"})
    privacy = fields.Integer(metadata={"description": "Current privacy of this object"})

    class Meta:
        ordered = True


class VendorDataProgression(Schema):
    progressionHash = fields.Integer(metadata={"description": "The progression for this vendor"})
    dailyProgress = fields.Integer(metadata={"description": "The daily progress for this vendor"})
    dailyLimit = fields.Integer(metadata={"description": "The daily limit for this vendor"})
    weeklyProgress = fields.Integer(metadata={"description": "The weekly progress for this vendor"})
    weeklyLimit = fields.Integer(metadata={"description": "The weekly limit for this vendor"})
    currentProgress = fields.Integer(metadata={"description": "The current progress for this vendor"})
    level = fields.Integer(metadata={"description": "The level reached for this vendor"})
    levelCap = fields.Integer(metadata={"description": "The max level for this vendor"})
    stepIndex = fields.Integer(metadata={"description": "The current step index for this vendor"})
    progressToNextLevel = fields.Integer(metadata={"description": "The XP needed to progress to next level for this vendor"})
    nextLevelAt = fields.Integer(metadata={"description": "The next level requirement for this vendor"})
    currentResetCount = fields.Integer(metadata={"description": "The number of rank reset for this vendor"})

    class Meta:
        ordered = True


class VendorData(Schema):
    canPurchase = fields.Boolean(metadata={"description": "Purchase status"})
    progression = fields.Dict(
        fields.String(), 
        fields.Nested(VendorDataProgression),
        allow_none=True,
        load_default=None,
        metadata={"description": "The current progression of the character"}
    )
    vendorLocationIndex = fields.Integer(metadata={"description": "The location of this vendor"})
    vendorHash = fields.Integer(metadata={"description": "The hash of the vendor"})
    nextRefreshDate = fields.String(metadata={"description": "The vendor's refresh date"})
    enabled = fields.Boolean(metadata={"description": "Is this vendor is enabled for this character"})

    class Meta:
        ordered = True


class Vendors(Schema):
    data = fields.Dict(
        fields.Integer(), 
        fields.Nested(VendorData),
        metadata={"description": "The data of a vendor"}
    )
    privacy = fields.Integer(metadata={"description": "Current privacy"})


class CategorieDataInfo(Schema):
    displayCategoryIndex = fields.Integer(metadata={"description": "The category index"})
    itemIndexes = fields.List(fields.Integer(), metadata={"description": "The index of item"})

    class Meta:
        ordered = True


class CategorieData(Schema):
    categories = fields.Nested(
        CategorieDataInfo, 
        many=True,
        metadata={"description": "The list of categories for a vendor"}
    )


class Categories(Schema):
    data = fields.Dict(
        fields.Integer(), 
        fields.Nested(CategorieData),
        metadata={"description": "The categorie of a vendor"},
        allow_none=True
    )
    privacy = fields.Integer(metadata={"description": "Current privacy"})

    class Meta:
        ordered = True


class CostInfo(Schema):
    itemHash = fields.Integer(metadata={"description": "The hash of the currency"})
    quantity = fields.Integer(metadata={"description": "The quantity required to buy the item"})
    hasConditionalVisibility = fields.Boolean()

    class Meta:
        ordered = True


class ItemInfo(Schema):
    saleStatus = fields.Integer()
    failureIndexes = fields.List(fields.Integer())
    augments = fields.Integer()
    vendorItemIndex = fields.Integer()
    itemHash = fields.Integer(metadata={"description": "The hash of the item"})
    quantity = fields.Integer(metadata={"description": "The quantity of the item you want to buy"})
    costs = fields.Nested(CostInfo, many=True, metadata={"description": "Costs of this item"})

    class Meta:
        ordered = True


class SalesItemsData(Schema):
    saleItems = fields.Dict(
        fields.Integer(),
        fields.Nested(ItemInfo),
        metadata={"description": "The list of items selled by the vendor"}
    )



class Sales(Schema):
    data = fields.Dict(
        fields.Integer(), 
        fields.Nested(SalesItemsData),
        metadata={"description": "The items selled by a vendor"},
        allow_none=True
    )
    privacy = fields.Integer(metadata={"description": "Current privacy"})

    class Meta:
        ordered = True


class VendorsReponseSchema(Schema):
    vendorGroups = fields.Nested(VendorGroups)
    vendors = fields.Nested(Vendors)
    categories = fields.Nested(Categories)
    sales = fields.Nested(Sales)

    class Meta:
        ordered = True
