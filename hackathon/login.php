<?php 
		session_start();
		include("db.php");
		
		  $user = $_SESSION['customer_mail'];

		  $getCustomerId = "SELECT customer_id FROM Customer WHERE customer_mail='$user'";
        $runQueryCid = mysqli_query($con, $getCustomerId);
        $row = mysqli_fetch_assoc($runQueryCid);
        $customer_id = $row['customer_id'];

		 
		  
            $f_name = $_POST['email'];
		    $sel_c = "INSERT into files values('$customer_id','$f_name')";
			
			$run_c = mysqli_query($con, $sel_c);
			
			if($run_c){
			$_SESSION['customer_mail']=$user; 
			echo "<script>alert('File created. Directing to form creation!')</script>";
			header("location: formCreation.html");
			}	
			else
			{
				
					echo "<script>alert('There is a problem, please try again!')</script>";
					// header("location: .html");
				

			}
            ?>
            
            