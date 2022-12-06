package rig.commons.handlers;

import lombok.Builder;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;
import rig.commons.utils.GuidGenerator;
import rig.commons.utils.IDGenerator;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * An interceptor class that populates dynamic context for a httpRequest
 */
@Component
@Builder
public class LogHandler extends HandlerInterceptorAdapter {

    private static final String GUID = "REQ_GUID";
    private static final String PREFIX = "GUID_PREFIX";

    @Builder.Default
    private static final IDGenerator guidGenerator = new GuidGenerator();
    @Builder.Default
    private static final DynamicContent mdc = new MDCwrapper();

    @Builder.Default
    private String messagePrefix = "request with id ";
    @Builder.Default
    private String incomingMessagePrefix = "request with incoming id ";
    @Builder.Default
    private String emptyMessagePrefix = "request with incoming empty id ";
    @Builder.Default
    private String headerName = "REQUEST_ID";

    /**
     * This implementation always returns true. It also populates the dynamic context
     * with two key-value pairs. Map entry for key "REQ_GUID" contains unique ID for the request
     * and map entry with key "GUID_PREFIX" contains a prefix string that can be used to differentiate if the
     * request ID was aquired from the incoming request's header or was generated anew or empty ID aquired from the incoming
     * request ID.
     * Private variables corresponding to such strings are named incomingMessagePrefix, messagePrefix and emptyMessagePrefix.
     * These can be set when creating LogHandler object by LogHandler.builder().
     * Their defaults are : "request with incoming id ", "request with id " and "request with incoming empty id ".
     *
     * @param request current HTTP request
     * @param response current HTTP response
     * @param handler chosen handler to execute
     * @return true if the execution chain should proceed with the next interceptor or the handler itself.
     * @throws Exception - in case of errors
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestId = request.getHeader(headerName);
        String guidPrefix;

        if (requestId == null) {
            requestId = String.valueOf(guidGenerator.getId());
            guidPrefix = messagePrefix;
        }
        else {
            guidPrefix = incomingMessagePrefix;

        }

        if (requestId.isEmpty()) {
            guidPrefix = emptyMessagePrefix;
        }

        mdc.put(PREFIX, guidPrefix);
        mdc.put(GUID, requestId);
        return super.preHandle(request, response, handler);
    }

    /**
     * @param request current HTTP request
     * @param response current HTTP response
     * @param handler that started the execution
     * @param modelAndView  that the handler returned (can also be null)
     * @throws Exception - in case of errors
     */
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        mdc.remove(GUID);
        mdc.remove(PREFIX);
        super.postHandle(request, response, handler, modelAndView);
    }
}

