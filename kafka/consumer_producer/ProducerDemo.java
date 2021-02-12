package tutorial1;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class ProducerDemo {
    public static void main(String[] args) {
        //System.out.println("hellow world!");

        // create Producer properties
        Properties properties = new Properties();
        // Old way of setting properties
        //properties.setProperty("bootstrap.servers", "localhost:9092");
        //properties.setProperty("bootstrap.servers", "127.0.0.1:9092");
        //properties.setProperty("key.serializer", StringSerializer.class.getName());
        //properties.setProperty("value.serializer", StringSerializer.class.getName());
        // New way of setting properties
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "127.0.0.1:9092");
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // create the producer
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(properties);

        // create a producer record
        ProducerRecord<String, String> record = new ProducerRecord<String, String>("first_topic", "second Java message");

        // send data - asynchronous, data is buffered, we must trigger data to
        // be sent by using flush() or close()ing the producer
        producer.send(record);

        // flush data
        producer.flush();
        // flush data and close producer
        producer.close();
    }
}
