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
 * An interceptor class that populates dynamic context for a httpRequest with specified header value under specified key
 *
 */
@Component
@Builder
public class GenericHeaderLogHandler extends HandlerInterceptorAdapter {


    @Builder.Default
    private static final DynamicContent mdc = new MDCwrapper();

    @Builder.Default
    private static final String nullValueString = "unknown";

    private String messagePrefix;

    private String headerName;

    private String key;

    /**
     * This implementation always returns true.      *
     * @param request current HTTP request
     * @param response current HTTP response
     * @param handler chosen handler to execute
     * @return true if the execution chain should proceed with the next interceptor or the handler itself.
     * @throws Exception - in case of errors
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String headerContent = request.getHeader(headerName);

        if (headerContent == null || headerContent.isEmpty()){
            headerContent = nullValueString;
        }
        mdc.put(key, messagePrefix+headerContent);
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
        mdc.remove(key);
        super.postHandle(request, response, handler, modelAndView);
    }
}

