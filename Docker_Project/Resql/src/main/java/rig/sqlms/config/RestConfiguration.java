package rig.sqlms.config;


import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ContentNegotiationConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import rig.commons.handlers.GenericHeaderLogHandler;
import rig.commons.handlers.LogHandler;

import static org.springframework.http.MediaType.APPLICATION_JSON;

@Configuration
@RequiredArgsConstructor
public class RestConfiguration implements WebMvcConfigurer {

    @Value("${userIPLoggingPrefix}")
    private String loggingPrefix = "from ip";
    @Value("${userIPHeaderName}")
    private String headerName = "x-forwarded-for";
    @Value("${userIPLoggingMDCkey}")
    private String key = "userIP";
    @Value("${cors.allowedOrigins:*}")
    private String allowedOrigins;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(LogHandler.builder().build());
        registry.addInterceptor(GenericHeaderLogHandler.builder()
                .key(key)
                .messagePrefix(loggingPrefix)
                .headerName(headerName)
                .build());
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins(allowedOrigins.split(","));
    }

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer.defaultContentType(APPLICATION_JSON);
    }
}
