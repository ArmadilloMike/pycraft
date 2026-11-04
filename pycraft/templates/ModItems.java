package {{ group_id }}.item;

import {{ group_id }}.{{ class_name }};
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    // Create the register for items
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(Registries.ITEM, {{ class_name }}.MODID);

{% for item in items %}
    {{ item.gen_java_code() }}
{% endfor %}

    // A method to hook this register into your main mod event bus
    public static void register(IEventBus eventBus) {
        ITEMS.register(eventBus);
    }
}
