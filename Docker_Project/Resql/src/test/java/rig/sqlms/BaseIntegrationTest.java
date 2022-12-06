package rig.sqlms;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import rig.sqlms.datasource.DataSourceContextHolder;
import rig.sqlms.datasource.RoutingDataSource;

import static java.util.Objects.requireNonNull;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

@ExtendWith(MockitoExtension.class)
@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SqlmsApplication.class, webEnvironment = RANDOM_PORT)
@AutoConfigureMockMvc(printOnlyOnFailure = false)
public abstract class BaseIntegrationTest {
    public static final Long ADMIN_ID = -1L;
    public static final String ADMIN_LOGIN = "admin";
    public static final String ADMIN_EMAIL = "admin@example.com";

    public static final String USER_LOGIN = "user";
    public static final String USER_EMAIL = "user@example.com";

    @LocalServerPort
    protected int port;
    @Autowired
    protected MockMvc mockMvc;
    @Autowired
    protected RoutingDataSource dataSource;

    @BeforeEach
    void beforeEach() {
        DataSourceContextHolder.setDataSourceName("crm");
        new ResourceDatabasePopulator(new ClassPathResource("init-crm-db.sql")).execute(requireNonNull(dataSource));
        DataSourceContextHolder.setDataSourceName("debt");
        new ResourceDatabasePopulator(new ClassPathResource("init-debt-db.sql")).execute(requireNonNull(dataSource));
        DataSourceContextHolder.clearDataSourceName();
    }

}
