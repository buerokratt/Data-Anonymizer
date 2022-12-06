package rig.commons.handlers;

/**
 * Interface with methods for accessing dynamic content
 */
public interface DynamicContent {

    String get(String key);
    void put(String key, String val);
    void remove(String key);

}
