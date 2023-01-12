package rig.commons.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/**
 * If a method is annotated as timed it's execution time is logged at debug level
 * If a class is annotated as timed all of it's public methods are timed
 */
@Aspect
@Component
@Slf4j
public class TimingAspect {

    @Pointcut("@within(Timed) && execution(public * *(..))")
    public void allPublicMethods() {
    }

    @Around("@annotation(Timed) || allPublicMethods()")
    public Object logExecutionTime(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        String timeStamp = getCurrentLocalDateTimeStamp(start);
        Object result = pjp.proceed();
        if (log.isDebugEnabled()) {
            log.debug("{} started at {}, execution took {} ms.",
                    pjp.getSignature().toShortString(), timeStamp, System.currentTimeMillis() - start);
        }
        return result;
    }


    private String getCurrentLocalDateTimeStamp(long epoch) {
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(epoch), ZoneId.systemDefault())
                .format(DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss.SSS"));
    }

}