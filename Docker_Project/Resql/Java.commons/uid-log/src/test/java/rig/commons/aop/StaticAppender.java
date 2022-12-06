package rig.commons.aop;

import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.AppenderBase;

import java.util.ArrayList;
import java.util.List;

public class StaticAppender extends AppenderBase<ILoggingEvent> {
    static List<String> events = new ArrayList<>();

    @Override
    public void append(ILoggingEvent e) {
        events.add(e.getFormattedMessage());

    }

    public static List<String> getEvents() {
        return events;
    }

    public static void clearEvents() {
        events.clear();
    }
}
