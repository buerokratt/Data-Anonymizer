package rig.commons.handlers;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.web.servlet.ModelAndView;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;


class LogHandlerTest {

    private LogHandler handler;
    private MockHttpServletRequest request;
    private MockHttpServletResponse response;
    private static final Object object = new Object();
    private static final ModelAndView modelAndView = new ModelAndView();
    private static final String PREFIX = "GUID_PREFIX";
    private static final String GUID = "REQ_GUID";

    @BeforeEach
    public void setUp() {
        handler = LogHandler.builder().build();
        request = new MockHttpServletRequest();
        response = new MockHttpServletResponse();
    }

    @Test
    void testThatKeyAddedToMDC() throws Exception {
        handler.preHandle(request, response, object);
        assertNotNull(MDC.get(GUID));
    }

    @Test
    void testThatKeyRemovedFromMDC() throws Exception {
        handler.postHandle(request, response, object, modelAndView);
        assertNull(MDC.get(GUID));
    }

    @Test
    void testDefaultMessagePrefix() throws Exception {
        handler.preHandle(request, response, object);
        assertEquals(MDC.get(PREFIX), "request with id ");
    }

    @Test
    void testDefaultIncomingMessagePrefix() throws Exception {
        request.addHeader("REQUEST_ID", "444");
        handler.preHandle(request, response, object);
        assertEquals(MDC.get(GUID), "444");
    }

    @Test
    void testDefaultEmptyMessagePrefix() throws Exception {
        request.addHeader("REQUEST_ID", "");
        handler.preHandle(request, response, object);
        assertEquals(MDC.get(PREFIX), "request with incoming empty id ");
    }

    @Test
    void testNONDefaultMessagePrefix() throws Exception {
        LogHandler builtHandler = LogHandler.builder().messagePrefix("NONDEFAULT").build();
        builtHandler.preHandle(request, response, object);
        assertEquals(MDC.get(PREFIX), "NONDEFAULT");
    }

    @Test
    void testNONDefaultIncomingMessagePrefix() throws Exception {
        request.addHeader("REQUEST_ID", "444");
        LogHandler builtHandler = LogHandler.builder().incomingMessagePrefix("NONDEFAULT").build();
        builtHandler.preHandle(request, response, object);
        assertEquals(MDC.get(PREFIX), "NONDEFAULT");
    }

    @Test
    void testNONDefaultEmptyMessagePrefix() throws Exception {
        request.addHeader("REQUEST_ID", "");
        LogHandler builtHandler = LogHandler.builder().emptyMessagePrefix("NONDEFAULT").build();
        builtHandler.preHandle(request, response, object);
        assertEquals(MDC.get(PREFIX), "NONDEFAULT");
    }

    @Test
    void testNONDefaultHeaderName() throws Exception {
        request.addHeader("NONDEFAULT", "444");
        LogHandler builtHandler = LogHandler.builder().headerName("NONDEFAULT").build();
        builtHandler.preHandle(request, response, object);
        assertEquals(MDC.get(GUID), "444");
    }

    @Test
    void testThreadSafety() throws Exception {
        List<String> strings = new ArrayList();
        Collection syncedStrings = Collections.synchronizedCollection(strings);
        handler = LogHandler.builder().build();
        Set<Thread> threads = new HashSet<>();

        for (int i = 0; i < 30_000; i++) {
            threads.add(
                    new Thread("" + i) {

                        public void run() {
                            request = new MockHttpServletRequest();
                            response = new MockHttpServletResponse();
                            try {
                                handler.preHandle(request, response, object);
                            } catch (Exception e) {
                                throw new RuntimeException();
                            }
                            syncedStrings.add(MDC.get("REQ_GUID"));
                        }
                    });
        }

        for (Thread t : threads) {
            t.start();
        }

        for (Thread t : threads) {
            t.join();
        }

        Set<String> set = new HashSet<>(strings);
        assertEquals(set.size(), syncedStrings.size());
    }

}
