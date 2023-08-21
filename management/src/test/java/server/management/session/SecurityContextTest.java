package server.management.session;

import org.junit.Assert;
import org.junit.Test;
import server.user.auth.AuthenticatedUser;
import server.user.auth.SecurityContext;
import server.user.autz.Role;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class SecurityContextTest {

    @Test
    public void context_shouldNotCollide_whenConcurrentActionOccurs() throws InterruptedException {
        CountDownLatch countDownLatch = new CountDownLatch(1);
        Runnable user1 = () -> {
            AuthenticatedUser currentUserToAdd = new AuthenticatedUser("ertugrul",
                    List.of(new Role("developer")));
            SecurityContext.addUserSession(currentUserToAdd);
            boolean await;
            try {
                await = countDownLatch.await(5, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                throw new RuntimeException("interrupted on awaiting", e);
            }
            if (!await) {
                throw new RuntimeException("timeout on awaiting");
            }

            AuthenticatedUser currentUser = SecurityContext.getCurrentUser();
            Assert.assertEquals(currentUserToAdd, currentUser);
        };

        Runnable user2 = () -> {
            AuthenticatedUser currentUserToAdd = new AuthenticatedUser("ahmet",
                    List.of(new Role("manager")));
            SecurityContext.addUserSession(currentUserToAdd);
            countDownLatch.countDown();
            AuthenticatedUser currentUser = SecurityContext.getCurrentUser();
            Assert.assertEquals(currentUserToAdd, currentUser);
        };

        Thread user1Thread = new Thread(user1);
        Thread user2Thread = new Thread(user2);
        user1Thread.start();
        user2Thread.start();
        user1Thread.join();
        user2Thread.join();
    }
}