package tutorial1;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class ProducerDemoWithCallback {
    public static void main(String[] args) {

        Logger logger = LoggerFactory.getLogger(ProducerDemoWithCallback.class);

        // create Producer properties
        Properties properties = new Properties();
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "127.0.0.1:9092");
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // create the producer
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(properties);

        for (int i=0; i<10; i++) {
            // create a producer record
            ProducerRecord<String, String> record =
                    new ProducerRecord<String, String>("first_topic", "Java message with Callback " + Integer.toString(i));

            // send data - asynchronous, data is buffered, we must trigger data to
            // be sent by using flush() or close()ing the producer
            producer.send(record, new Callback() {
                @Override
                // onCompletion executes every time a record is successfully sent or an exception is thrown
                public void onCompletion(RecordMetadata recordMetadata, Exception e) {
                    if (e == null) {
                        // record was successfully sent
                        logger.info("Received new metadata: \n" +
                                "Topic: " + recordMetadata.topic() + "\n" +
                                "Partition: " + recordMetadata.partition() + "\n" +
                                "Offset: " + recordMetadata.offset() + "\n" +
                                "Timestamp: " + recordMetadata.timestamp() + "\n"
                        );
                    } else {
                        logger.error("Error while producing", e);
                    }
                }
            });
        }

        // flush data
        producer.flush();
        // flush data and close producer
        producer.close();
    }
}
