package rig.commons.utils;

/**
 Interface that contains method for getting a long ID
 @see GuidGenerator for example of implementation
 */
public interface IDGenerator {

    /**
     * @return unique ID
     */
    public long getId();

}
