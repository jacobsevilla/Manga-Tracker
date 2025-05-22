class Manga:
    # ** class Variables
    # Total number of series collected
    total_series_collection_count = 0
    # Total number of volumes collected
    total_volume_collection_count = 0
    # Total price of volumes collected
    total_collection_price = 0

    def __init__(self, title, volumes_owned, total_volumes, price_per_volume, is_serializing, is_misc):
        self.title = title
        self.volumes_owned = volumes_owned
        self.total_volumes = total_volumes
        self.price_per_volume = price_per_volume
        self.is_serializing = is_serializing
        self.is_misc = is_misc
        
        # Update total number of series collected
        Manga.total_series_collection_count += 1

        # Update total number of volumes collected
        Manga.total_volume_collection_count += volumes_owned

        # Update total collection price
        Manga.total_collection_price += self.total_series_price
    
    # Total series price needs a getter method
    @property # ** @property
    def total_series_price(self):
        return self.volumes_owned * self.price_per_volume
    
    def collection_status(self):
        if self.is_misc:
            return "Art books etc."
        elif self.volumes_owned == self.total_volumes and not self.is_serializing:
            return "Completed"
        elif self. volumes_owned < self.total_volumes and not self.is_serializing:
            return "Incomplete"
        else:
            return "Ongoing"
    
    @classmethod # ** classmethod
    def get_total_series_collection_count(cls):
        return cls.total_series_collection_count
    
    @classmethod
    def get_total_volume_collection_count(cls):
        return cls.total_volume_collection_count
    
    @classmethod
    def get_total_collection_price(cls):
        return cls.total_collection_price
    
