package rig.commons.utils;

import java.util.concurrent.atomic.AtomicLong;

/**
 * class for generating timestamp based unique numerical IDs.
 */
public class GuidGenerator implements IDGenerator {

    private static AtomicLong LAST_TIME_MS = new AtomicLong();

    /**
     @see IDGenerator#getId()
     @return Id which is as close representation of milliseconds from epoch as can be returned as unique.
     If there is more than one request for getId() per ms then the requests are resolved sequentially
     incrementing the value by one for each next one.
     */
    public long getId() {
        long now = System.currentTimeMillis();
        while (true) {
            long lastTime = LAST_TIME_MS.get();
            if (lastTime >= now)
                now = lastTime + 1;
            if (LAST_TIME_MS.compareAndSet(lastTime, now))
                return now;
        }
    }
}
