package {{ group_id }};

import {{ group_id }}.item.ModItems;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod({{ class_name }}.MODID)
public class {{ class_name }} {
    public static final String MODID = "{{ mod_id }}";

    public {{class_name}}(IEventBus modEventBus) {
        ModItems.register(modEventBus);
    }
}
