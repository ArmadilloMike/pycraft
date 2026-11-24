package {{ group_id }}.item;

import {{ group_id }}.{{ class_name }};
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.minecraft.world.item.Rarity;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.common.SimpleTier;

public class ModItems {
    // Create the register for items
    public static final DeferredRegister.Items ITEMS =
        DeferredRegister.createItems({{ class_name }}.MODID);

{% for item in items %}
    {% if item.food_properties is not none %}
        {{ item.food_properties.gen_food_properties_line(item.item_id) }}
    {% endif %}
    {% if item.item_material is not none %}
        {{ item.item_material.gen_java_code() }}
    {% endif %}
    {{ item.gen_java_code() }}
{% endfor %}

    // A method to hook this register into your main mod event bus
    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}
