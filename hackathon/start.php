<?php 
		session_start();
		include("db.php");
		// if(isset($_POST['Login'])){
		// }
		
        
        $c_mail = $_POST['email'];
			$c_pass = $_POST['pass'];
			
			$sel_c = "SELECT * from Customer where customer_password='$c_pass' AND customer_mail='$c_mail'";
			
			$run_c = mysqli_query($con, $sel_c);
			
			$check_customer = mysqli_num_rows($run_c); 

            //echo $check_customer;
			if($check_customer>0 ){
			$_SESSION['customer_mail']=$c_mail; 
			header("location: after_login.html");
			}	
            else{
                echo "<script>alert('Email or password is incorrect, please go back and try again!')</script>";
				//header("location: start.html");
            }
            ?>
            
            