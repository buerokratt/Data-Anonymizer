package rig.commons.utils;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotEquals;


class GuidGeneratorTest {

    private GuidGenerator guidGenerator;

    @BeforeEach
    public void setup() {
        this.guidGenerator = new GuidGenerator();
    }

    @Test
    void testGetID() {
        assertNotEquals(guidGenerator.getId(), guidGenerator.getId());
    }

}
