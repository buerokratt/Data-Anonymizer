package rig.commons.aop;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.reflect.MethodSignature;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TimingAspectTest {

    @Mock
    private ProceedingJoinPoint proceedingJoinPoint;
    private final TimingAspect aspect = new TimingAspect();
    private final MethodSignature signature = mock(MethodSignature.class);

    @BeforeEach
    public void setUp() {
        when(proceedingJoinPoint.getSignature()).thenReturn(signature);
        when(signature.toShortString()).thenReturn("TESTSIGNATURE");
    }

    @Test
    void testLogging() throws Throwable {
        aspect.logExecutionTime(proceedingJoinPoint);
        String pattern = "TESTSIGNATURE started at (\\d\\d\\.){2}\\d{4} (\\d\\d:){2}\\d\\d\\.\\d{3}" +
                         ", execution took \\d+ ms\\.";
        String logString = StaticAppender.getEvents().get(0);
        assertTrue(logString.matches(pattern));
    }
}
