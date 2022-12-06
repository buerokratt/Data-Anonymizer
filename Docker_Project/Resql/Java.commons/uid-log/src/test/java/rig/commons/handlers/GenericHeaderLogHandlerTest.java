package rig.commons.handlers;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.web.servlet.ModelAndView;

import static org.junit.jupiter.api.Assertions.*;


class GenericHeaderLogHandlerTest {

    private GenericHeaderLogHandler handler;
    private MockHttpServletRequest request;
    private MockHttpServletResponse response;
    private static final Object object = new Object();
    private static final ModelAndView modelAndView = new ModelAndView();
    private static final String PREFIX = "request originating from ip: ";
    private static final String KEY = "ORIG_IP";
    private static final String HEADERNAME = "x-forwarded-for";

    @BeforeEach
    public void setUp() {
        handler = GenericHeaderLogHandler.builder().headerName(HEADERNAME).messagePrefix(PREFIX).key(KEY).build();
        request = new MockHttpServletRequest();
        response = new MockHttpServletResponse();
    }

    @Test
    void testThatKeyAddedToMDC() throws Exception {
        handler.preHandle(request, response, object);
        assertNotNull(MDC.get(KEY));
    }

    @Test
    void testThatKeyRemovedFromMDC() throws Exception {
        handler.postHandle(request, response, object, modelAndView);
        assertNull(MDC.get(KEY));
    }

    @Test
    void testNANString() throws Exception {
        handler.preHandle(request, response, object);
        assertEquals(MDC.get(KEY), PREFIX + "unknown");
    }

    @Test
    void testHappyPath() throws Exception {
        request.addHeader(HEADERNAME, "s");
        handler.preHandle(request, response, object);
        assertEquals(MDC.get(KEY), PREFIX + "s");
    }

}
