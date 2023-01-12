package rig.commons.handlers;

import org.slf4j.MDC;

/**
 * Wrapper for org.slf4j.MDC implementing DynamicContent interface which is used by LogHandler
 * @see DynamicContent
 * @see LogHandler
 */
public class MDCwrapper implements DynamicContent {

    /**
     *
     * @param key map key
     * @return string that was mapped to the key
     */
    @Override
    public String get(String key) {
        return MDC.get(key);
    }

    /**
     *
     * @param key map key
     * @param val map value
     * Inserts a key-value pair
     */
    @Override
    public void put(String key, String val) {
        MDC.put(key, val);
    }

    /**
     * @param key map key
     * removes map entry for the key
     */
    @Override
    public void remove(String key) {
        MDC.remove(key);
    }
}
